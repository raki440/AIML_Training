"""raw csv -> clean -> features -> validate -> processed parquet.
Run from the project root:  python scripts/run_pipeline.py
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mlkit import cleaning, features, validation
from mlkit.config import DATA_PROCESSED, DATA_RAW, SEED
from mlkit.data_io import read_table, write_table
from mlkit.logger import get_logger
from mlkit.utils import set_seed

log = get_logger("pipeline")

SCHEMA = {
    "customer_id": {},
    "tenure_months": {"min": 1, "max": 120},
    "monthly_charges": {"min": 0},
    "logins_per_week": {"min": 0},
    "support_tickets": {"min": 0},
    "plan": {"allowed": {"basic", "standard", "premium"}},
    "churn": {"allowed": {0, 1}},
    "tickets_per_month": {"min": 0},
}


def run(input_path, output_path):
    set_seed(SEED)
    df = read_table(input_path)
    df = cleaning.standardize_columns(df)
    df = cleaning.clean_text(df, ["plan"])
    df = cleaning.drop_duplicates(df)
    df = cleaning.fill_missing(df, ["monthly_charges"])
    df = cleaning.clip_outliers(df, "monthly_charges")
    df = features.add_features(df)
    validation.validate(df, SCHEMA)
    write_table(df, output_path)
    log.info("profile: %s", validation.data_profile(df))
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=DATA_RAW / "customers.csv")
    ap.add_argument("--output", default=DATA_PROCESSED / "customers1.csv")
    args = ap.parse_args()
    run(args.input, args.output)
