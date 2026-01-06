from dataclasses import dataclass
from typing import Any, Dict

from shared.schemas.edge_controller.receive_telemetry.receive_telemetry_input import (
    ReceiveTelemetryInput,
)


@dataclass
class ReceiveTelemetryInputDTO(ReceiveTelemetryInput):
    edge_id: str
    device_id: str
    device_type: str
    timestamp: str
    metrics: Dict[str, float]
    meta: Dict[str, Any] | None = None
