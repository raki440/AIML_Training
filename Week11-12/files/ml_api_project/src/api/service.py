"""Load the saved model ONCE and score customers."""

import json
import logging
from pathlib import Path

import joblib
import pandas as pd
import sklearn

from src.features import add_features
from src.train import METADATA_FILE, MODEL_FILE

log = logging.getLogger("churn-api")


def risk_label(probability: float) -> str:
    if probability >= 0.7:
        return "high"
    return "medium" if probability >= 0.3 else "low"


class ModelService:
    def __init__(self, model, metadata: dict):
        self.model = model
        self.metadata = metadata

    @classmethod
    def load(cls, model_dir) -> "ModelService":
        model_dir = Path(model_dir)
        model_path = model_dir / MODEL_FILE
        if not model_path.exists():
            raise RuntimeError(
                f"Model not found at {model_path}. Run training first: python -m src.train"
            )
        meta_path = model_dir / METADATA_FILE
        metadata = json.loads(meta_path.read_text()) if meta_path.exists() else {}
        trained_with = metadata.get("sklearn_version")
        if trained_with and trained_with != sklearn.__version__:
            log.warning(
                "model trained with scikit-learn %s, running %s", trained_with, sklearn.__version__
            )
        return cls(joblib.load(model_path), metadata)

    @property
    def version(self) -> str:
        return self.metadata.get("model_version", "unknown")

    def predict_proba(self, customers: list[dict]) -> list[float]:
        df = add_features(pd.DataFrame(customers))
        return [round(float(p), 3) for p in self.model.predict_proba(df)[:, 1]]
