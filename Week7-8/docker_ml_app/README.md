# Containerized ML app: churn model

Train a small churn model and score customers, first locally, then in Docker, then with Docker Compose.

## Run locally (no Docker)
    pip install -r requirements-dev.txt
    python -m pytest
    python -m src.train
    python -m src.predict

## Docker: single image
    docker build -t churn-app:1.0 .
    docker run --rm churn-app:1.0                       # stops: no model in a fresh container
    docker run --rm -v models:/app/models churn-app:1.0 python -m src.train
    docker run --rm -v models:/app/models churn-app:1.0 # predicts from the saved model

On Windows, put each command on one line.

## Single-stage vs multi-stage
    docker build -f Dockerfile.single -t churn-app:single .
    docker build -t churn-app:1.0 .
    docker images churn-app                             # compare SIZE
    docker history churn-app:1.0
    docker build --target builder -t churn-app:builder .   # stop at the first stage

Optional: uncomment the `build-essential` line in BOTH Dockerfiles, rebuild, and compare sizes again.

## Docker Compose
    docker compose up --build        # train first, then predict
    docker compose logs
    docker compose ps -a
    docker volume ls                 # the models volume (prefixed with the project name)
    docker compose down              # stop and remove containers, keep the volume
    docker compose down -v           # also remove the volume

## Files
| File | Purpose |
|---|---|
| `src/` | features, train, predict |
| `Dockerfile` | multi-stage build (the image we ship) |
| `Dockerfile.single` | single-stage version for comparison |
| `.dockerignore` | files kept out of the build context |
| `compose.yaml` | train and predict services sharing a `models` volume |

## Troubleshooting
- `Model not found`: train first, and mount the same volume for both commands.
- `Permission denied` writing to `/app/models`: the folder must be owned by `appuser` (see the `chown` line in the Dockerfile) and the volume must be a named volume, not a bind mount.
- Build is slow every time: keep `COPY requirements.txt` and `RUN pip install` above `COPY src/`.
