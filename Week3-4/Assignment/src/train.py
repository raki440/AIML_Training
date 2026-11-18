
"""Train a small churn model and save it to MODEL_DIR.
Run: python -m src.train
"""
import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.features import CATEGORICAL, NUMERIC, add_features

MODEL_DIR = Path(os.getenv("MODEL_DIR", "models"))
SEED = int(os.getenv("SEED", "42"))
MODEL_FILE = "churn_model.joblib"


def make_data(n: int = 3000, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "tenure_months": rng.integers(1, 72, n),
        "monthly_charges": rng.normal(70, 20, n).clip(20, 150).round(2),
        "logins_per_week": rng.poisson(5, n),
        "support_tickets": rng.poisson(1.5, n),
        "plan": rng.choice(["basic", "standard", "premium"], n, p=[.5, .3, .2]),
    })
    logit = (
        -0.5 - 0.04 * df.tenure_months
        + 0.015 * df.monthly_charges
        - 0.25 * df.logins_per_week
        + 0.5 * df.support_tickets
        + 0.6 * (df.plan == "basic")
    )
    df["churn"] = (
        rng.random(n) < 1 / (1 + np.exp(-logit))
    ).astype(int)
    df.loc[
        rng.choice(n, int(.03 * n), replace=False),
        "monthly_charges"
    ] = np.nan
    return df


def train(model_dir=MODEL_DIR, seed: int = SEED) -> dict:
    df = add_features(make_data(seed=seed))
    X, y = df[NUMERIC + CATEGORICAL], df["churn"]

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=seed
    )

    pre = ColumnTransformer([
        (
            "num",
            Pipeline([
                ("imp", SimpleImputer(strategy="median")),
                ("sc", StandardScaler())
            ]),
            NUMERIC
        ),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])

    model = Pipeline([
        ("pre", pre),
        ("model", LogisticRegression(max_iter=1000))
    ]).fit(X_tr, y_tr)

    auc = float(
        roc_auc_score(y_te, model.predict_proba(X_te)[:, 1])
    )

    model_dir = Path(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_dir / MODEL_FILE)

    return {
        "auc": round(auc, 3),
        "rows": len(df),
        "saved_to": str(model_dir / MODEL_FILE)
    }


if __name__ == "__main__":
    print(f"Training started with SEED={SEED}")
    result = train()
    print(result)
