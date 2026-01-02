from dataclasses import dataclass

from shared.schemas.edge_controller.forward_telemetry.telemetry_output import TelemetryOutput


@dataclass(frozen=True)
class ForwardTelemetryOutputDTO(TelemetryOutput):
    forwarded: bool

'''
@dataclass(frozen=True)
class ForwardTelemetryOutputDTO:
    forwarded: bool
'''