
from ....infrastructure.clients.management_client import ManagementClient
from .input_dto import ReportCommandResultInputDTO


class ReportCommandResultUseCase:
    def __init__(self, management_client: ManagementClient):
        self.management_client = management_client

    def execute(self, dto: ReportCommandResultInputDTO):
        self.management_client.send_command_result(dto.result_payload)
