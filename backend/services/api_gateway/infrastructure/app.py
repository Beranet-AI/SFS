"""Application entrypoint for the monitoring service."""

from __future__ import annotations

from fastapi import FastAPI
from api.routes import register_routes


def create_app() -> FastAPI:
    app = FastAPI(title="api_gateway")
    register_routes(app)
    return app
