import pandas as pd


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """'Monthly Charges ' -> 'monthly_charges'."""
    out = df.copy()
    out.columns = (out.columns.str.strip().str.lower()
                   .str.replace(r"[^0-9a-z]+", "_", regex=True).str.strip("_"))
    return out


def clean_text(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Strip spaces and lowercase text columns so ' Basic' and 'basic' match."""
    out = df.copy()
    for c in columns:
        out[c] = out[c].str.strip().str.lower()
    return out


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates().reset_index(drop=True)


def fill_missing(df: pd.DataFrame, columns: list[str], strategy: str = "median") -> pd.DataFrame:
    """Fill NaNs with the median, mean or mode of each column."""
    if strategy not in {"median", "mean", "mode"}:
        raise ValueError(f"unknown strategy: {strategy}")
    out = df.copy()
    for c in columns:
        value = out[c].mode().iloc[0] if strategy == "mode" else getattr(out[c], strategy)()
        out[c] = out[c].fillna(value)
    return out


def clip_outliers(df: pd.DataFrame, column: str, lower_q: float = 0.01, upper_q: float = 0.99) -> pd.DataFrame:
    """Cap extreme values at the given quantiles."""
    out = df.copy()
    lo, hi = out[column].quantile([lower_q, upper_q])
    out[column] = out[column].clip(lo, hi)
    return out
