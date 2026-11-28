from pathlib import Path

import pandas as pd

from mlkit.logger import get_logger

log = get_logger(__name__)


def read_table(path) -> pd.DataFrame:
    """Read a .csv or .parquet file; fail early with a clear message."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No such file: {path}")
    df = pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_csv(path)
    log.info("read %d rows x %d cols from %s", df.shape[0], df.shape[1], path.name)
    return df


def write_table(df: pd.DataFrame, path) -> Path:
    """Write a .csv or .parquet file, creating folders as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        df.to_parquet(path, index=False)
    else:
        df.to_csv(path, index=False)
    log.info("wrote %d rows to %s", len(df), path)
    return path
