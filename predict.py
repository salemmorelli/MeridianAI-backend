from __future__ import annotations

import logging
from pathlib import Path

import joblib
import pandas as pd

from catalog import load_catalog
from config import get_settings

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
settings = get_settings()
MODEL_PATH = (
    Path(settings.model_path)
    if Path(settings.model_path).is_absolute()
    else BASE_DIR / settings.model_path
)


def _build_point_details() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in load_catalog()["points"]:
        entry: dict[str, str] = {
            "name": p["name"],
            "location": p["location"],
            "technique": p["howTo"],
        }
        who = p.get("whoCode")
        if who:
            entry["who_code"] = who
        out[p["id"]] = entry
    return out


def _build_default_by_symptom() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for p in reversed(load_catalog()["points"]):
        for raw in p.get("benefits", []) + p.get("matchKeywords", []):
            key = raw.lower().strip()
            if key:
                mapping[key] = p["id"]
    return mapping


def _build_default_by_region() -> dict[str, str]:
    defaults = (load_catalog().get("defaults") or {}).get("byRegion") or {}
    return {str(k).lower(): str(v) for k, v in defaults.items()}


POINT_DETAILS = _build_point_details()
DEFAULT_BY_SYMPTOM = _build_default_by_symptom()
DEFAULT_BY_REGION = _build_default_by_region()


class ModelNotReadyError(RuntimeError):
    pass


def load_model():
    if not MODEL_PATH.exists():
        raise ModelNotReadyError(
            "Model file not found. Run `python train.py` first to generate model.joblib."
        )
    logger.info("Loading model from %s", MODEL_PATH)
    return joblib.load(MODEL_PATH)


def predict_best_point(symptom: str, region: str, duration_minutes: int) -> dict:
    symptom_normalized = symptom.lower().strip()
    region_normalized = region.lower().strip()

    if symptom_normalized == "all" and region_normalized == "all":
        raise ValueError("Please provide at least one of symptom or region.")

    if symptom_normalized != "all" and region_normalized == "all":
        point_code = DEFAULT_BY_SYMPTOM.get(symptom_normalized, "LI4")
    elif symptom_normalized == "all" and region_normalized != "all":
        point_code = DEFAULT_BY_REGION.get(region_normalized, "LI4")
    else:
        model = load_model()
        features = pd.DataFrame(
            [
                {
                    "symptom": symptom_normalized,
                    "region": region_normalized,
                    "duration_minutes": duration_minutes,
                }
            ]
        )
        point_code = model.predict(features)[0]

    details = POINT_DETAILS.get(point_code, {})
    who = details.get("who_code", point_code)
    return {
        "point_code": point_code,
        "who_point_code": who,
        "point_name": details.get("name", point_code),
        "location": details.get("location", "Unknown"),
        "technique": details.get("technique", "No technique available."),
    }
