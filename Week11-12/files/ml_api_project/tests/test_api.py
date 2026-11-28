import pytest
import json
from fastapi.testclient import TestClient

from src.api.main import create_app
from src.train import train

RISKY = {
    "tenure_months": 3,
    "monthly_charges": 95,
    "logins_per_week": 1,
    "support_tickets": 4,
    "plan": "basic",
}
LOYAL = {
    "tenure_months": 60,
    "monthly_charges": 60,
    "logins_per_week": 9,
    "support_tickets": 0,
    "plan": "premium",
}


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    model_dir = tmp_path_factory.mktemp("models")
    train(model_dir)
    with TestClient(create_app(model_dir)) as test_client:  # "with" runs the lifespan
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_v1_response_shape(client):
    body = client.post("/v1/predict", json=RISKY).json()
    assert set(body) == {"score"} and 0 <= body["score"] <= 1


def test_v2_response_shape_and_risk(client):
    risky = client.post("/v2/predict", json=RISKY).json()
    loyal = client.post("/v2/predict", json=LOYAL).json()

    expected_fields = {
        "churn_probability",
        "risk",
        "model_version",
        "prediction_status",
    }

    assert set(risky) == expected_fields
    assert set(loyal) == expected_fields

    assert risky["risk"] == "high"
    assert loyal["risk"] == "low"

    assert risky["prediction_status"] == "completed"
    assert loyal["prediction_status"] == "completed"


def test_invalid_input_is_422(client):
    assert client.post("/v1/predict", json={**RISKY, "plan": "gold"}).status_code == 422
    assert client.post("/v2/predict", json={**RISKY, "tenure_months": 0}).status_code == 422


def test_batch_endpoints(client):
    v1 = client.post("/v1/predict/batch", json={"customers": [RISKY, LOYAL]}).json()
    v2 = client.post("/v2/predict/batch", json={"customers": [RISKY, LOYAL]}).json()
    assert len(v1["scores"]) == 2 and len(v2["predictions"]) == 2
    assert client.post("/v1/predict/batch", json={"customers": []}).status_code == 422


def test_response_names_the_instance(client):
    assert client.get("/health").headers["x-served-by"]


def test_startup_fails_clearly_without_a_model(tmp_path):
    with pytest.raises(RuntimeError, match="Run training first"):
        with TestClient(create_app(tmp_path)):
            pass

def test_v1_model_info(client):
    response = client.get("/v1/model-info")

    assert response.status_code == 200

    metadata_path = client.app.state.model_dir / "metadata.json"
    expected_metadata = json.loads(
        metadata_path.read_text(encoding="utf-8")
    )

    assert response.json() == expected_metadata