# api/routes/management_telemetry.py
from fastapi import APIRouter, HTTPException, status
from .base import router as base_router

from ...application.services.edge_service import EdgeService
from ...mappers.telemetry_mapper import (
    InboundTelemetryMapper,
)

  
router = APIRouter(prefix="/telemetry", tags=["telemetry"])

edge_service = EdgeService()


@router.post(
    "",
    summary="Receive telemetry from device",
    description="Forward telemetry from approved devices to management-telemetry"
)
def receive_telemetry(payload: dict):
    try:
        telemetry_dto = InboundTelemetryMapper.to_input(payload)

        edge_service.handle_telemetry(telemetry_dto)

        return {"status": "ACCEPTED"}

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing field: {str(e)}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Telemetry forwarding failed: {str(e)}",
        )


base_router.include_router(router)
