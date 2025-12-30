# application/use_cases/validate_telemetry/output_dto.py

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ValidateTelemetryOutputDTO:
    domain_telemetry: Dict[str, Any]
    schema_version: str
