"""Score customers with the saved model.  Run: python -m src.predict [customers.json]"""

import json
import sys
from pathlib import Path

import joblib
import pandas as pd

from src.features import add_features
from src.train import MODEL_DIR, MODEL_FILE

SAMPLES = [
    {
        "tenure_months": 3,
        "monthly_charges": 95,
        "logins_per_week": 1,
        "support_tickets": 4,
        "plan": "basic",
    },
    {
        "tenure_months": 60,
        "monthly_charges": 60,
        "logins_per_week": 9,
        "support_tickets": 0,
        "plan": "premium",
    },
]


def load_model(model_dir=MODEL_DIR):
    path = Path(model_dir) / MODEL_FILE
    if not path.exists():
        raise SystemExit(f"Model not found at {path}. Run training first: python -m src.train")
    return joblib.load(path)


def predict(customers: list[dict], model_dir=MODEL_DIR) -> list[float]:
    df = add_features(pd.DataFrame(customers))
    return [round(float(p), 3) for p in load_model(model_dir).predict_proba(df)[:, 1]]


if __name__ == "__main__":
    customers = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else SAMPLES
    print(json.dumps({"model_dir": str(MODEL_DIR), "scores": predict(customers)}, indent=2))
