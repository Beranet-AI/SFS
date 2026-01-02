from .receive_telemetry_input import ReceiveTelemetryInput
from .receive_telemetry_output import ReceiveTelemetryOutput


class ReceiveTelemetryUseCase:
    def execute(self, input_dto: ReceiveTelemetryInput) -> ReceiveTelemetryOutput:
        return ReceiveTelemetryOutput(payload=input_dto.payload)
