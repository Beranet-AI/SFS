from ....infrastructure.clients.management_client import ManagementClient
from .input_dto import SendResultInputDTO


class SendResultUseCase:
    """
    Report command execution result from edge to management service
    """

    def __init__(self, management_client: ManagementClient):
        self.management_client = management_client

    def execute(self, dto: SendResultInputDTO):
        """
        Translate DTO to payload expected by ManagementClient
        """

        payload = {
            "command_id": dto.command_id,
            "command_type": dto.command_type,
            "status": dto.status,
            "executed_at": dto.executed_at.isoformat(),
            "payload": dto.payload,
        }

        self.management_client.send_command_result(payload)
