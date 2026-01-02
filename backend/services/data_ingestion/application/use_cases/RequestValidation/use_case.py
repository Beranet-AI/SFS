from .request_validation_input import RequestValidationInput
from .request_validation_output import RequestValidationOutput
from ....infrastructure.clients.management_telemetry_client import (
    ManagementTelemetryClient,
)


class RequestValidationUseCase:
    def __init__(self, client: ManagementTelemetryClient | None = None) -> None:
        self._client = client or ManagementTelemetryClient()

    def execute(self, input_dto: RequestValidationInput) -> RequestValidationOutput:
        response = self._client.request_validation(input_dto.payload)
        return RequestValidationOutput(
            valid=response.get("valid", False),
            details=response.get("details"),
        )
