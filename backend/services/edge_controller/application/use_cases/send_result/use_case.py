from ....infrastructure.clients.commands_client import CommandsClient
from .input_dto import SendResultInputDTO


class SendResultUseCase:
    """
    Report command execution result from edge to management service
    """

    def __init__(self, commands_client: CommandsClient):
        self.commands_client = commands_client

    def execute(self, dto: SendResultInputDTO):
        """
        Translate DTO to payload expected by CommandsClient
        """

        payload = {
            "command_id": dto.command_id,
            "command_type": dto.command_type,
            "status": dto.status,
            "executed_at": dto.executed_at.isoformat(),
            "payload": dto.payload,
        }

        self.commands_client.send_command_result(payload)
