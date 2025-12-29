from ....infrastructure.clients.data_ingestion_client import DataIngestionClient
from .input_dto import TelemetryInputDTO


class ForwardTelemetryUseCase:
    def __init__(self, data_ingestion_client: DataIngestionClient):
        self.data_ingestion_client = data_ingestion_client

    def execute(self, dto: TelemetryInputDTO):
        self.data_ingestion_client.send_telemetry(dto.to_dict())
