from fastapi import APIRouter, Depends, HTTPException, status

from ....application.use_cases.receive_telemetry.input_dto import (
    ReceiveTelemetryInputDTO,
)
from ....application.use_cases.receive_telemetry.use_case import (
    ReceiveTelemetryUseCase,
)
from ..dependencies.use_cases import get_receive_telemetry_use_case
from ..schemas.receive_telemetry_request import ReceiveTelemetryRequest
from ..schemas.receive_telemetry_response import ReceiveTelemetryResponse

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


@router.post(
    "",
    summary="Receive telemetry from device",
    description="Forward telemetry from approved devices to management",
    response_model=ReceiveTelemetryResponse,
)
def receive_telemetry(
    payload: ReceiveTelemetryRequest,
    use_case: ReceiveTelemetryUseCase = Depends(get_receive_telemetry_use_case),
) -> ReceiveTelemetryResponse:
    try:
        dto = ReceiveTelemetryInputDTO(
            edge_id=payload.edge_id,
            device_id=payload.device_id,
            device_type=payload.device_type,
            timestamp=payload.timestamp.isoformat().replace("+00:00", "Z"),
            metrics=payload.metrics,
            meta=payload.meta,
        )
        result = use_case.execute(dto)
        return ReceiveTelemetryResponse(status=result.status)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Telemetry forwarding failed: {exc}",
        ) from exc
