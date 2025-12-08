"""Application entrypoint for the data ingestion service."""

from __future__ import annotations

from fastapi import FastAPI
from api.routes import register_routes


def create_app() -> FastAPI:
    app = FastAPI(title="device_controller")
    register_routes(app)
    return app
