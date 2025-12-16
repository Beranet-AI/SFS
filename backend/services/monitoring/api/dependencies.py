"""Dependency injection wiring for the monitoring API layer."""

from __future__ import annotations

from .schemas.health import HealthResponse
from ..application.health_service import HealthService, HealthServiceProtocol


def get_health_service() -> HealthServiceProtocol:
    """Provide the health service implementation for monitoring endpoints."""

    return HealthService()


__all__ = ["get_health_service", "HealthResponse"]
