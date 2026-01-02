from ....infrastructure.clients.data_ingestion_client import (
    DataIngestionClient,
)
from .send_telemetry_input import SendTelemetryInput
from .send_telemetry_output import SendTelemetryOutput


class SendTelemetryUseCase:
    def __init__(self, client: DataIngestionClient | None = None) -> None:
        self._client = client or DataIngestionClient()

    def execute(self, input_dto: SendTelemetryInput) -> SendTelemetryOutput:
        for item in input_dto.standardized:
            self._client.send_telemetry(item)
        return SendTelemetryOutput(sent=True)
