# application/use_cases/receive_telemetry/input_dto.py

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ReceiveTelemetryInputDTO:
    source: str
    device_id: str
    payload: Dict[str, Any]
    received_at: int
    metadata: Dict[str, Any]
