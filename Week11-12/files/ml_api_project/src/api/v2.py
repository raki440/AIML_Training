from fastapi import APIRouter, Request

from src.api.schemas import BatchRequest, BatchV2, Customer, PredictionV2
from src.api.service import risk_label

router = APIRouter(prefix="/v2", tags=["v2"])

def _prediction(probability: float, version: str) -> PredictionV2:
    return PredictionV2(
        churn_probability=probability,
        risk=risk_label(probability),
        model_version=version,
        prediction_status="completed"
    )


@router.post("/predict", response_model=PredictionV2)
def predict(customer: Customer, request: Request):
    service = request.app.state.service
    probability = service.predict_proba([customer.model_dump()])[0]
    return _prediction(probability, service.version)


@router.post("/predict/batch", response_model=BatchV2)
def predict_batch(body: BatchRequest, request: Request):
    service = request.app.state.service
    probabilities = service.predict_proba([c.model_dump() for c in body.customers])
    return BatchV2(predictions=[_prediction(p, service.version) for p in probabilities])
