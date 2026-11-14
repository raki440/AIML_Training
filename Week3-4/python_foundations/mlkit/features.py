import numpy as np
import pandas as pd

from mlkit.config import SEED


def add_ratio(df: pd.DataFrame, numerator: str, denominator: str, name: str) -> pd.DataFrame:
    """New column = numerator / denominator (division by zero becomes NaN)."""
    out = df.copy()
    out[name] = out[numerator] / out[denominator].replace(0, np.nan)
    return out


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Single place for feature logic: reuse it in training AND serving."""
    return add_ratio(df, "support_tickets", "tenure_months", "tickets_per_month")


def split_xy(df: pd.DataFrame, target: str):
    return df.drop(columns=target), df[target]


def train_test_split_df(df: pd.DataFrame, test_size: float = 0.2, seed: int = SEED):
    """Reproducible shuffle split. Returns (train, test)."""
    idx = np.random.default_rng(seed).permutation(len(df))
    n_test = int(len(df) * test_size)
    return df.iloc[idx[n_test:]].reset_index(drop=True), df.iloc[idx[:n_test]].reset_index(drop=True)
