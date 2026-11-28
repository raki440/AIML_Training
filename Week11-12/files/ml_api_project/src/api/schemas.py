from typing import Literal

from pydantic import BaseModel, Field


class Customer(BaseModel):
    tenure_months: int = Field(ge=1, le=120)
    monthly_charges: float = Field(ge=0)
    logins_per_week: int = Field(ge=0)
    support_tickets: int = Field(ge=0)
    plan: Literal["basic", "standard", "premium"]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tenure_months": 3,
                    "monthly_charges": 95,
                    "logins_per_week": 1,
                    "support_tickets": 4,
                    "plan": "basic",
                }
            ]
        }
    }


class BatchRequest(BaseModel):
    customers: list[Customer] = Field(min_length=1, max_length=1000)


# ---- v1 responses ----
class PredictionV1(BaseModel):
    score: float


class BatchV1(BaseModel):
    scores: list[float]


# ---- v2 responses (the field is renamed, so this is a breaking change: new version) ----
class PredictionV2(BaseModel):
    churn_probability: float
    risk: Literal["low", "medium", "high"]
    model_version: str
    prediction_status: str


class BatchV2(BaseModel):
    predictions: list[PredictionV2]
