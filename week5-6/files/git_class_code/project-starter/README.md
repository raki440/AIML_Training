# Churn project: Git workflow practice

Small Python project for practising the GitHub workflow in a team of 2-3.

## Tasks
1. One person creates the repo on GitHub and adds the others as collaborators. Push this starter to `main`.
2. Turn on branch protection for `main`: require a pull request and the CI check. (On a free GitHub account this needs a public repository.)
3. Each person creates a feature branch (e.g. `feature/<name>-<task>`), makes small commits, pushes, opens a pull request.
4. Review each other's pull requests. Ask for at least one change.
5. Two people edit the same line of this README on purpose, then resolve the conflict.
6. Merge everything into `main` and tag the result `v0.1`.

## Run the tests
    pip install -r requirements.txt
    python -m pytest
