"""Application entrypoint for the data ingestion service."""

from __future__ import annotations

from fastapi import FastAPI

from api.routes import register_routes


def create_app() -> FastAPI:
    """Construct and configure the FastAPI application instance."""

    app = FastAPI(title="data_ingestion")
    register_routes(app)
    return app
