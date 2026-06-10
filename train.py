from __future__ import annotations

import logging
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

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


def build_training_data() -> pd.DataFrame:
    rows: list[dict] = []
    for p in load_catalog()["points"]:
        pid = p["id"]
        region = (p.get("visual") or {}).get("region") or "leg"
        terms = [s for s in p.get("benefits", []) + p.get("matchKeywords", []) if str(s).strip()]
        for sym in {t.lower().strip() for t in terms}:
            for dur in (1, 2, 3):
                rows.append(
                    {"symptom": sym, "region": region, "duration_minutes": dur, "label": pid}
                )
    return pd.DataFrame(rows)


def train_and_save_model() -> Path:
    df = build_training_data()
    x = df[["symptom", "region", "duration_minutes"]]
    y = df["label"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["symptom", "region"]),
            ("num", "passthrough", ["duration_minutes"]),
        ]
    )
    
    model = Pipeline(
         steps=[
             ("preprocessor", preprocessor),
             ("classifier", RandomForestClassifier(
                 n_estimators=100,
                max_depth=8,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
             )),
        ]
    ) 
    model.fit(x, y)
    # Log feature importance
    feature_names = (
        model.named_steps["preprocessor"]
        .get_feature_names_out()
        .tolist()
    )

    importances = model.named_steps["classifier"].feature_importances_
    top_features = sorted(
        zip(feature_names, importances),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    logger.info("Top 10 most important features:")
    for name, score in top_features:
        logger.info("  %-40s %.4f", name, score)

    joblib.dump(model, MODEL_PATH)
    return MODEL_PATH


if __name__ == "__main__":
    output = train_and_save_model()
    logger.info("Model saved to: %s", output)
