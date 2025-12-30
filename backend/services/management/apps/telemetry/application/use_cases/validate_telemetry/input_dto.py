# application/use_cases/validate_telemetry/input_dto.py

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ValidateTelemetryInputDTO:
    raw_payload: Dict[str, Any]
    device_type: str
    schema_version: str | None = None
