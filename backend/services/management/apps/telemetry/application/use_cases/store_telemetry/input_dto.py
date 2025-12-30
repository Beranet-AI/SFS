# application/use_cases/store_telemetry/input_dto.py

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class StoreTelemetryInputDTO:
    device_id: str
    source: str
    schema_version: str
    telemetry_data: Dict[str, Any]
    received_at: int
