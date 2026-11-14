import pandas as pd

from mlkit import features


def test_add_ratio_handles_zero():
    df = pd.DataFrame({"a": [4, 4], "b": [2, 0]})
    out = features.add_ratio(df, "a", "b", "r")
    assert out["r"].iloc[0] == 2 and pd.isna(out["r"].iloc[1])


def test_split_sizes_and_reproducible():
    df = pd.DataFrame({"x": range(100)})
    tr1, te1 = features.train_test_split_df(df, 0.2, seed=1)
    tr2, te2 = features.train_test_split_df(df, 0.2, seed=1)
    assert len(tr1) == 80 and len(te1) == 20
    assert te1.equals(te2)
