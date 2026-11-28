"""Create a deliberately messy customer file: data/raw/customers.csv"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd

from mlkit.config import DATA_RAW, SEED, ensure_dirs


def make_raw_customers(n: int = 3000, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "Customer ID": np.arange(1, n + 1),
        "Tenure Months": rng.integers(1, 72, n),
        "Monthly Charges": rng.normal(70, 20, n).clip(20, 150).round(2),
        "Logins Per Week": rng.poisson(5, n),
        "Support Tickets": rng.poisson(1.5, n),
        "Plan": rng.choice(["Basic", "standard", "PREMIUM"], n, p=[.5, .3, .2]),
    })
    logit = (-0.5 - 0.04 * df["Tenure Months"] + 0.015 * df["Monthly Charges"]
             - 0.25 * df["Logins Per Week"] + 0.5 * df["Support Tickets"] + 0.6 * (df["Plan"] == "Basic"))
    df["Churn"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    # mess: missing values, extreme values, untidy text
    df.loc[rng.choice(n, int(.03 * n), replace=False), "Monthly Charges"] = np.nan
    df.loc[rng.choice(n, 5, replace=False), "Monthly Charges"] = 9999.0
    df.loc[rng.choice(n, 10, replace=False), "Plan"] = " basic "
    return pd.concat([df, df.sample(25, random_state=1)], ignore_index=True)


if __name__ == "__main__":
    ensure_dirs()
    path = DATA_RAW / "customers.csv"
    make_raw_customers().to_csv(path, index=False)
    print("wrote", path)
