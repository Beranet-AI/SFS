"""Route registration for the monitoring API layer."""

from __future__ import annotations

from fastapi import FastAPI

from . import health
from .. import events


def register_routes(app: FastAPI) -> None:
    """Attach API routers to the FastAPI instance."""

    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(events.router, prefix="/monitoring", tags=["monitoring"])
