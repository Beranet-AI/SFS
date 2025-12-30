# application/use_cases/receive_telemetry/output_dto.py

from dataclasses import dataclass


@dataclass
class ReceiveTelemetryOutputDTO:
    telemetry_id: str
    status: str
