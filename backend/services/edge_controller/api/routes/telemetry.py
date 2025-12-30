# api/routes/telemetry.py
from fastapi import APIRouter, HTTPException, status
from .base import router as base_router

from ...application.services.edge_service import EdgeService
from ...mappers.telemetry_mapper import (
    InboundTelemetryMapper,
    OutboundTelemetryMapper,
)
from ...application.use_cases.forward_telemetry.output_dto import (
    ForwardTelemetryOutputDTO,
)

  
router = APIRouter(
    prefix="/telemetry",
    tags=["telemetry"]
)

edge_service = EdgeService()


@router.post(
    "",
    summary="Receive telemetry from device",
    description="Forward telemetry from approved devices to data_ingestion"
)
def receive_telemetry(payload: dict):
    try:

        telemetry_dto = InboundTelemetryMapper.to_input(payload)

        edge_service.handle_telemetry(telemetry_dto)

        return OutboundTelemetryMapper.to_response(
            ForwardTelemetryOutputDTO(forwarded=True)
        )

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
