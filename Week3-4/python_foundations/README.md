# Python foundations toolkit (Weeks 3-4)

Reusable building blocks for the end-to-end MLOps project: paths, logging, seeds, data I/O, cleaning, features, validation, tests.

## Structure
    mlkit/            reusable code (import mlkit)
      config.py       paths and settings        logger.py     logging
      utils.py        set_seed                  data_io.py    read/write csv, parquet
      cleaning.py     clean data                features.py   features and split
      validation.py   schema checks, profile
    scripts/          make_sample_data.py, run_pipeline.py
    tests/            pytest tests
    notebooks/        01 Python basics, 02 NumPy, 03 pandas and data manipulation
    requirements.txt  numpy, pandas, pyarrow, pytest

## Setup
macOS / Linux

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Windows (Command Prompt)

    py -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

One command on macOS / Linux: `bash setup_env.sh` (create env, install, test, run pipeline).

## Run
    python -m pytest
    python scripts/make_sample_data.py
    python scripts/run_pipeline.py        # data/raw/customers.csv -> data/processed/customers.parquet

Notebooks: `pip install jupyter`, then open the files in `notebooks/` (run them from that folder).
