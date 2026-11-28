"""Churn API.  Run: uvicorn src.api.main:app --reload   (docs at /docs)"""

import os
import socket
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from src.api import v1, v2
from src.api.service import ModelService
from src.train import MODEL_DIR


def create_app(model_dir=MODEL_DIR) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.service = ModelService.load(model_dir)  # load once, at startup
        yield

    app = FastAPI(title="Churn API", version="2.0.0", lifespan=lifespan)
    
    app.state.model_dir = model_dir
    @app.middleware("http")
    async def add_instance_header(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Served-By"] = os.getenv("INSTANCE_NAME", socket.gethostname())
        return response

    @app.get("/health")
    def health(request: Request):
        return {"status": "ok", "model_version": request.app.state.service.version}

    app.include_router(v1.router)
    app.include_router(v2.router)
    return app


app = create_app()
