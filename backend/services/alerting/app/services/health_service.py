"""Health service abstractions for the alerting context."""

from __future__ import annotations

from typing import Protocol

from ..domain import HealthStatus


class HealthServiceProtocol(Protocol):
    """Contract for providing service health information."""

    def check_health(self) -> HealthStatus:
        """Return the current service health status."""


class HealthService(HealthServiceProtocol):
    """Default implementation that reports local service health."""

    def check_health(self) -> HealthStatus:
        return HealthStatus(status="ok", message="alerting service is healthy")


__all__ = ["HealthServiceProtocol", "HealthService"]
