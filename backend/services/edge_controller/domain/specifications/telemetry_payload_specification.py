from ..exceptions.validation_error import DomainValidationError


class TelemetryPayloadSpecification:
    def validate(self, payload: dict) -> None:
        if not payload.get("metrics"):
            raise DomainValidationError("Telemetry metrics cannot be empty")

        if "timestamp" not in payload:
            raise DomainValidationError("Telemetry timestamp is required")
