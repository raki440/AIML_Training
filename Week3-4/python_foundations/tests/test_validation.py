import pandas as pd
import pytest

from mlkit.validation import ValidationError, data_profile, validate

SCHEMA = {"age": {"min": 0, "max": 120}, "plan": {"allowed": {"a", "b"}}}


def test_valid_data_passes():
    validate(pd.DataFrame({"age": [10, 20], "plan": ["a", "b"]}), SCHEMA)


def test_reports_all_problems():
    bad = pd.DataFrame({"age": [-1, 200], "plan": ["a", "z"]})
    with pytest.raises(ValidationError) as e:
        validate(bad, SCHEMA)
    msg = str(e.value)
    assert "below 0" in msg and "above 120" in msg and "outside" in msg


def test_missing_column_and_profile():
    with pytest.raises(ValidationError):
        validate(pd.DataFrame({"age": [1]}), SCHEMA)
    assert data_profile(pd.DataFrame({"x": [1, 1, None]}))["duplicates"] == 1
