from ....infrastructure.clients.management_telemetry_client import (
    ManagementTelemetryClient,
)
from .input_dto import TelemetryInputDTO


class ForwardTelemetryUseCase:
    def __init__(self, management_telemetry_client: ManagementTelemetryClient):
        self.management_telemetry_client = management_telemetry_client

    def execute(self, dto: TelemetryInputDTO):
        self.management_telemetry_client.send_raw_telemetry(dto.to_dict())
