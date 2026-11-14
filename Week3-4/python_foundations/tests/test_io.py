import pandas as pd
import pytest

from mlkit.data_io import read_table, write_table


@pytest.mark.parametrize("name", ["t.csv", "t.parquet"])
def test_roundtrip(tmp_path, name):
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    write_table(df, tmp_path / "sub" / name)
    assert read_table(tmp_path / "sub" / name).equals(df)


def test_missing_file_message(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_table(tmp_path / "nope.csv")
