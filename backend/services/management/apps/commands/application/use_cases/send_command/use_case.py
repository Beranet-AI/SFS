import uuid

from apps.commands.application.services.command_api_service import (
    CommandApiService,
)
from .input_dto import SendCommandInputDTO


class SendCommandUseCase:

    def __init__(self, service: CommandApiService | None = None):
        self._service = service or CommandApiService()

    def execute(self, *, device_id: str, action: str):
        command = {
            "command": "device_command",
            "command_id": str(uuid.uuid4()),
            "device_id": device_id,
            "action": action,
        }

        # Stub: MQTT / HTTP
        print("[SEND DEVICE COMMAND]", command)

        return command["command_id"]

    def create_command(self, dto: SendCommandInputDTO, *, created_by: str):
        return self._service.create_command(
            data=dto.to_dict(),
            created_by=created_by,
        )

    def get_command(self, *, command_id: str):
        return self._service.get_command(command_id=command_id)

    def ack_command(self, *, data: dict):
        self._service.ack_command(data=data)
