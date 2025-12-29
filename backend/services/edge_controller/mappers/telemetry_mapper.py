# mapper/telemetry_mapper.py
from datetime import datetime
from ..application.use_cases.forward_telemetry.input_dto import TelemetryInputDTO


def raw_telemetry_to_dto(
    *,
    edge_id: str,
    device_id: str,
    device_type: str,
    metrics: dict,
    meta: dict | None = None,
) -> TelemetryInputDTO:
    """
    Map raw telemetry from device listener to TelemetryInputDTO
    """

    return TelemetryInputDTO(
        edge_id=edge_id,
        device_id=device_id,
        device_type=device_type,
        timestamp=datetime.utcnow(),
        metrics=metrics,
        meta=meta,
    )
