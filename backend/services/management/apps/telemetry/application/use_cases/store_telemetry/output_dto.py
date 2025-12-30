# application/use_cases/store_telemetry/output_dto.py

from dataclasses import dataclass


@dataclass
class StoreTelemetryOutputDTO:
    telemetry_id: str
