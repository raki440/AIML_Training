import pandas as pd


class ValidationError(ValueError):
    """Raised when data breaks the schema."""


def validate(df: pd.DataFrame, schema: dict) -> None:
    """Check columns, nulls, ranges and allowed values. Reports ALL problems at once.

    schema = {"age": {"min": 0, "max": 120}, "plan": {"allowed": {"a", "b"}, "nullable": False}}
    """
    errors = []
    for col, rule in schema.items():
        if col not in df.columns:
            errors.append(f"missing column: {col}")
            continue
        s = df[col]
        if not rule.get("nullable", False) and s.isna().any():
            errors.append(f"{col}: {int(s.isna().sum())} missing values")
        values = s.dropna()
        if "min" in rule and (values < rule["min"]).any():
            errors.append(f"{col}: values below {rule['min']}")
        if "max" in rule and (values > rule["max"]).any():
            errors.append(f"{col}: values above {rule['max']}")
        if "allowed" in rule and (~values.isin(rule["allowed"])).any():
            errors.append(f"{col}: values outside {sorted(rule['allowed'])}")
    if errors:
        raise ValidationError("; ".join(errors))


def data_profile(df: pd.DataFrame) -> dict:
    """Small summary to log, or to keep as a baseline for later drift checks."""
    return {"rows": len(df), "columns": df.shape[1],
            "missing": df.isna().sum()[lambda s: s > 0].to_dict(),
            "duplicates": int(df.duplicated().sum())}
