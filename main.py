from __future__ import annotations

import logging
import time

from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import case, func
from sqlalchemy.orm import Session as DBSession

import models
from config import get_settings
from feedback_store import init_feedback_db
from llm_triage import triage_symptom_text
from predict import ModelNotReadyError, predict_best_point

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("meridianai")

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled exception on {request.method} {request.url}: {exc}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again."},
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    logger.info(
        f"{request.method} {request.url.path} "
        f"→ {response.status_code} ({duration}ms)"
    )
    return response


class PredictionRequest(BaseModel):
    symptom: str = Field(..., example="headache")
    region: str = Field(..., example="hand")
    duration_minutes: int = Field(1, ge=1, le=10, example=2)


class FeedbackRequest(BaseModel):
    session_id: str = Field(..., min_length=3, max_length=100)
    symptom: str = Field(..., example="headache")
    region: str = Field(..., example="neck")
    selected_meridian: str | None = Field(None, example="gallbladder")
    duration_minutes: int = Field(1, ge=1, le=10, example=2)
    recommended_point: str = Field(..., example="GB20")
    helped: bool = Field(..., description="True if recommendation helped")


class LlmTriageRequest(BaseModel):
    symptom_text: str = Field(..., min_length=3, example="I feel neck pain and headache")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: PredictionRequest) -> dict:
    try:
        result = predict_best_point(
            symptom=payload.symptom,
            region=payload.region,
            duration_minutes=payload.duration_minutes,
        )
    except ModelNotReadyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected prediction error: {exc}") from exc

    return {
        "input": payload.model_dump(),
        "recommendation": result,
    }


@app.on_event("startup")
def startup() -> None:
    logger.info("Starting %s", settings.app_name)
    Base.metadata.create_all(bind=engine)
    init_feedback_db()


@app.post("/feedback")
def feedback(payload: FeedbackRequest, db: DBSession = Depends(get_db)) -> dict:
    try:
        record = models.Feedback(**payload.model_dump())
        db.add(record)
        db.commit()
        db.refresh(record)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not save feedback: {exc}") from exc
    return {"status": "ok", "feedback_id": record.id}


@app.get("/feedback/summary")
def feedback_summary(db: DBSession = Depends(get_db)) -> dict:
    total = db.query(func.count(models.Feedback.id)).scalar() or 0
    helped = (
        db.query(func.count(models.Feedback.id))
        .filter(models.Feedback.helped.is_(True))
        .scalar()
        or 0
    )
    point_rows = (
        db.query(
            models.Feedback.recommended_point,
            func.count().label("total_count"),
            func.sum(case((models.Feedback.helped.is_(True), 1), else_=0)).label("helped_count"),
        )
        .group_by(models.Feedback.recommended_point)
        .order_by(func.count().desc())
        .all()
    )
    return {
        "total_feedback": int(total),
        "helped_feedback": int(helped),
        "help_rate": (float(helped) / float(total)) if total else 0.0,
        "points": [
            {
                "recommended_point": row.recommended_point,
                "total_count": row.total_count,
                "helped_count": int(row.helped_count or 0),
            }
            for row in point_rows
        ],
    }


@app.post("/llm-triage")
def llm_triage(payload: LlmTriageRequest) -> dict:
    try:
        result = triage_symptom_text(payload.symptom_text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Triage failed: {exc}") from exc
    return {"input": payload.model_dump(), "triage": result}

