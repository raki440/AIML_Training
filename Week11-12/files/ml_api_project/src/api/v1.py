from fastapi import APIRouter, Request

from src.api.schemas import BatchRequest, BatchV1, Customer, PredictionV1

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/predict", response_model=PredictionV1)
def predict(customer: Customer, request: Request):
    score = request.app.state.service.predict_proba([customer.model_dump()])[0]
    return PredictionV1(score=score)


@router.post("/predict/batch", response_model=BatchV1)
def predict_batch(body: BatchRequest, request: Request):
    scores = request.app.state.service.predict_proba([c.model_dump() for c in body.customers])
    return BatchV1(scores=scores)
