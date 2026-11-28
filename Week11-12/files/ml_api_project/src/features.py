import pandas as pd

NUMERIC = [
    "tenure_months",
    "monthly_charges",
    "logins_per_week",
    "support_tickets",
    "tickets_per_month",
]
CATEGORICAL = ["plan"]


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """One feature function, used by training AND prediction (no train/serve skew)."""
    out = df.copy()
    out["tickets_per_month"] = out["support_tickets"] / out["tenure_months"]
    return out
