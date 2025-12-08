"""API response DTOs for alerting health endpoints."""

from __future__ import annotations

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Represents the API-facing health payload."""

    status: str
    message: str


__all__ = ["HealthResponse"]
