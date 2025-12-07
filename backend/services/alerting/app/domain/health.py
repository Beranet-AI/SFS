"""Domain objects for expressing alerting service health."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthStatus:
    """Represents the domain-level health status for the service."""

    status: str
    message: str


__all__ = ["HealthStatus"]
