# Churn model as an API (continues the Weeks 9-10 CI/CD project)

The churn model from earlier weeks, served with FastAPI, with two API versions, a Docker image and an nginx load balancer.

## What is new
| Path | Purpose |
|---|---|
| `src/api/main.py` | app factory, startup (load model once), `/health`, `X-Served-By` header |
| `src/api/schemas.py` | request validation and the v1 / v2 response models |
| `src/api/service.py` | `ModelService`: loads the model, scores customers |
| `src/api/v1.py`, `v2.py` | the two versions, mounted at `/v1` and `/v2` |
| `src/train.py` | now also writes `metadata.json` (model version, library version, features) |
| `scripts/load_demo.py` | counts which replica answered each request |
| `nginx.conf`, `compose.yaml` | train, then `api` replicas behind nginx on port 8080 |
| `tests/test_api.py` | API tests (also run by the CI workflows from Weeks 9-10) |

## Run locally
    pip install -r requirements-dev.txt
    python -m pytest
    python -m src.train
    uvicorn src.api.main:app --reload       # open http://localhost:8000/docs

## Endpoints
| Method and path | Body | Response |
|---|---|---|
| `GET /health` | | `{"status": "ok", "model_version": "1.0.0"}` |
| `POST /v1/predict` | one customer | `{"score": 0.952}` |
| `POST /v1/predict/batch` | `{"customers": [...]}` | `{"scores": [...]}` |
| `POST /v2/predict` | one customer | `{"churn_probability": 0.952, "risk": "high", "model_version": "1.0.0"}` |
| `POST /v2/predict/batch` | `{"customers": [...]}` | `{"predictions": [...]}` |

Customer: `tenure_months` (1-120), `monthly_charges` (>= 0), `logins_per_week` (>= 0), `support_tickets` (>= 0), `plan` (`basic`, `standard` or `premium`). Invalid input returns 422.

    curl -s -X POST localhost:8000/v2/predict -H "Content-Type: application/json" \
      -d '{"tenure_months":3,"monthly_charges":95,"logins_per_week":1,"support_tickets":4,"plan":"basic"}'

(On Windows, use the `/docs` page instead of curl.)

## Docker Compose with a load balancer
    docker compose up --build --scale api=3
    python scripts/load_demo.py --url http://localhost:8080 --n 30    # requests per replica
    docker compose ps
    docker stop <one api container>                                   # then run load_demo again
    docker compose down -v

Compose runs `train` first, starts the `api` replicas when training succeeded, and starts nginx when the replicas are healthy. Only nginx publishes a port (8080); the replicas just `expose` 8000, because several replicas cannot share one host port.

nginx resolves the name `api` when it starts and balances across every address it gets (round robin by default). After changing the number of replicas, restart nginx: `docker compose restart nginx`.

## Notes
- Model files are loaded with joblib: only load files you trust, and load them with the same scikit-learn version that saved them. The API logs a warning if `metadata.json` shows a different version.
- Each container runs one uvicorn process; scale by running more containers.
- Test client: current Starlette asks for `httpx2` (`httpx` still works with a warning).
- Not run in Docker while preparing this project: build and run the Compose stack once yourself. The app, the tests and the nginx round robin were tested locally.
