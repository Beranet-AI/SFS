"""Health routes for the alerting service."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from ..dependencies import HealthResponse, get_health_service
from ...services.health_service import HealthServiceProtocol

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check(
    health_service: HealthServiceProtocol = Depends(get_health_service),
) -> HealthResponse:
    """Return service availability status using the domain service."""

    status = health_service.check_health()
    return HealthResponse(status=status.status, message=status.message)
