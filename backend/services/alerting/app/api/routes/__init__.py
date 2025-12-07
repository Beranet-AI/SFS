"""Route registration for the alerting API layer."""

from __future__ import annotations

from fastapi import FastAPI

from . import health


def register_routes(app: FastAPI) -> None:
    """Attach API routers to the FastAPI instance."""

    app.include_router(health.router, prefix="/health", tags=["health"])
