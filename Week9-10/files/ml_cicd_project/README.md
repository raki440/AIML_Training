# ML CI/CD project (continues the Weeks 7-8 Docker app)

The same churn app, now with automation: lint, tests, a model quality gate and a Docker image build, all on GitHub Actions.

## What is new
| Path | Purpose |
|---|---|
| `.github/workflows/ci.yml` | `lint`, `test` (Python 3.11 and 3.12), then `model-check` |
| `.github/workflows/docker.yml` | build the image on pull requests; push to `ghcr.io` on `main` and `v*` tags |
| `.github/dependabot.yml` | weekly update pull requests for actions and pip packages |
| `scripts/check_metrics.py` | quality gate: fails if AUC is below a minimum |
| `pyproject.toml` | ruff and coverage settings |
| `workflow-examples/01_hello.yml` | first workflow for Demo 1 (copy to `.github/workflows/`) |

## Run the same checks locally
    pip install -r requirements-dev.txt
    ruff check .
    ruff format --check .
    python -m pytest --cov --cov-fail-under=80
    python -m src.train
    python scripts/check_metrics.py --min-auc 0.75      # OK
    python scripts/check_metrics.py --min-auc 0.9       # FAIL, exit code 1

## Put it on GitHub
1. Create a repository and push this folder to `main`.
2. Open the Actions tab and watch `CI` and `Docker` run.
3. Settings, Branches: protect `main` and require the checks (`lint`, `test (3.11)`, `test (3.12)`, `model-check`). The check names appear after the first run.
4. Work through pull requests (Demo 2 to Demo 4).

## Notes
- The workflows use `actions/checkout@v7`, `actions/setup-python@v7`, `actions/upload-artifact@v7`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/metadata-action@v6` and `docker/build-push-action@v7`. Check each action's Marketplace page for the current major version before class.
- The Docker image is `ghcr.io/<owner>/<repo>` (lowercase). If `docker pull` is denied, log in with `docker login ghcr.io` or check the package's visibility settings.
- The app, Dockerfiles and `compose.yaml` are unchanged from Weeks 7-8, except that training now also writes `metrics.json`.
