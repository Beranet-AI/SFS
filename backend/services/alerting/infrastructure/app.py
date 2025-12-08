"""Application entrypoint for the alerting service."""

from __future__ import annotations

from fastapi import FastAPI

from api.routes import register_routes


def create_app() -> FastAPI:
    """Construct and configure the FastAPI application instance."""

    app = FastAPI(title="alerting")
    register_routes(app)
    return app
