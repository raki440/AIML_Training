import numpy as np
import pandas as pd

from mlkit import cleaning


def test_standardize_columns():
    df = pd.DataFrame(columns=[" Monthly Charges ", "Customer-ID"])
    assert list(cleaning.standardize_columns(df).columns) == ["monthly_charges", "customer_id"]


def test_clean_text():
    df = pd.DataFrame({"plan": [" Basic", "PREMIUM ", None]})
    assert cleaning.clean_text(df, ["plan"])["plan"].tolist()[:2] == ["basic", "premium"]


def test_drop_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2]})
    assert len(cleaning.drop_duplicates(df)) == 2


def test_fill_missing_median_and_no_mutation():
    df = pd.DataFrame({"x": [1.0, np.nan, 3.0]})
    assert cleaning.fill_missing(df, ["x"])["x"].tolist() == [1.0, 2.0, 3.0]
    assert df["x"].isna().sum() == 1


def test_clip_outliers():
    df = pd.DataFrame({"x": list(range(100)) + [10_000]})
    assert cleaning.clip_outliers(df, "x")["x"].max() < 10_000
