from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

from feedback_store import get_helpful_feedback_rows, init_feedback_db
from train import MODEL_PATH, build_training_data


def build_dataset_with_feedback() -> pd.DataFrame:
    base_df = build_training_data()
    init_feedback_db()
    helpful = get_helpful_feedback_rows()
    if not helpful:
        return base_df

    feedback_rows = [
        {
            "symptom": r["symptom"],
            "region": r["region"],
            "duration_minutes": int(r["duration_minutes"] or 2),
            "label": r["recommended_point"],
        }
        for r in helpful
    ]
    feedback_df = pd.DataFrame(feedback_rows)
    return pd.concat([base_df, feedback_df], ignore_index=True)


def retrain_model() -> Path:
    df = build_dataset_with_feedback()
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
            ("classifier", DecisionTreeClassifier(random_state=42, max_depth=6)),
        ]
    )
    model.fit(x, y)
    joblib.dump(model, MODEL_PATH)
    return MODEL_PATH


if __name__ == "__main__":
    path = retrain_model()
    print(f"Retrained model saved to: {path}")
