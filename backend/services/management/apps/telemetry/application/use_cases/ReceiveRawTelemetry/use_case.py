from .receive_raw_telemetry_input import ReceiveRawTelemetryInput
from .receive_raw_telemetry_output import ReceiveRawTelemetryOutput


class ReceiveRawTelemetryUseCase:
    def execute(
        self, input_dto: ReceiveRawTelemetryInput
    ) -> ReceiveRawTelemetryOutput:
        return ReceiveRawTelemetryOutput(
            payload=input_dto.payload, source=input_dto.source
        )
