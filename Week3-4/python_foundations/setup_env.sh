#!/usr/bin/env bash
# macOS / Linux: create the environment, install, test, run the pipeline.
set -e
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest -q
python scripts/make_sample_data.py
python scripts/run_pipeline.py
