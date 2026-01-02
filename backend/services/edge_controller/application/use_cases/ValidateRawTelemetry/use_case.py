from .validate_raw_telemetry_input import ValidateRawTelemetryInput
from .validate_raw_telemetry_output import ValidateRawTelemetryOutput
from ....validators.telemetry_validator import validate_telemetry_payload


class ValidateRawTelemetryUseCase:
    def execute(
        self, input_dto: ValidateRawTelemetryInput
    ) -> ValidateRawTelemetryOutput:
        validate_telemetry_payload(input_dto.payload)
        return ValidateRawTelemetryOutput(valid=True)
