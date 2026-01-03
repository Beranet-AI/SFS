from .input_dto import ReceiveTelemetryInput
from .output_dto import ReceiveTelemetryOutput


class ReceiveTelemetryUseCase:
    def execute(self, input_dto: ReceiveTelemetryInput) -> ReceiveTelemetryOutput:
        return ReceiveTelemetryOutput(payload=input_dto.payload)
