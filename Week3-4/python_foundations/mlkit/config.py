"""Project paths and settings in one place."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"
SEED = int(os.getenv("SEED", "42"))


def ensure_dirs() -> None:
    for p in (DATA_RAW, DATA_INTERIM, DATA_PROCESSED):
        p.mkdir(parents=True, exist_ok=True)
