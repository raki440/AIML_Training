import pandas as pd


def fill_missing(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Return a copy of df with missing values in `column` replaced by the median."""
    out = df.copy()
    out[column] = out[column].fillna(out[column].median())
    return out
