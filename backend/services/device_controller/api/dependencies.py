"""Dependency injection wiring for API routes."""

from __future__ import annotations

from .schemas.health import HealthResponse
from ..services.health_service import HealthService, HealthServiceProtocol


def get_health_service() -> HealthServiceProtocol:
    """Provide the health service implementation.

    Keeping the provider in a dedicated module makes it easy to swap the
    implementation (e.g., a cached or distributed health checker) without
    modifying the route handlers.
    """

    return HealthService()


__all__ = ["get_health_service", "HealthResponse"]
