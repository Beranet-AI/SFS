from dataclasses import dataclass

from shared.schemas.edge_controller.receive_telemetry.receive_telemetry_output import (
    ReceiveTelemetryOutput,
)


@dataclass
class ReceiveTelemetryOutputDTO(ReceiveTelemetryOutput):
    status: str
