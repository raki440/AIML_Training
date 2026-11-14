import pandas as pd

from src.clean import fill_missing


def test_fill_missing_uses_median():
    df = pd.DataFrame({"x": [1.0, None, 3.0]})
    assert fill_missing(df, "x")["x"].tolist() == [1.0, 2.0, 3.0]


def test_original_is_not_changed():
    df = pd.DataFrame({"x": [1.0, None, 3.0]})
    fill_missing(df, "x")
    assert df["x"].isna().sum() == 1
