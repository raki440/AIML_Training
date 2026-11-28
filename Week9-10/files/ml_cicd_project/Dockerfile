# syntax=docker/dockerfile:1
# Multi-stage build: stage 1 builds the environment, stage 2 is the small image we ship.

# ---------- Stage 1: builder ----------
FROM python:3.11-slim AS builder
WORKDIR /build
# If a dependency must be compiled, install build tools HERE (builder only):
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.11-slim AS runtime
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_DIR=/app/models
RUN useradd --create-home --shell /usr/sbin/nologin appuser
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY src/ ./src/
RUN mkdir -p "$MODEL_DIR" && chown -R appuser:appuser /app
USER appuser
CMD ["python", "-m", "src.predict"]
