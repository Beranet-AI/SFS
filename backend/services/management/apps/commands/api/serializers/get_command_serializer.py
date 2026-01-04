from rest_framework import serializers

from apps.commands.api.serializers.actions.send_command_serializer import (
    command_to_output,
)
from apps.commands.application.use_cases.get_command.input_dto import (
    GetCommandInputDTO,
)
from apps.commands.application.use_cases.get_command.output_dto import (
    GetCommandOutputDTO,
)
from apps.commands.domain.entities.command import Command


class GetCommandSerializer(serializers.Serializer):
    command_id = serializers.UUIDField()

    def to_input_dto(self) -> GetCommandInputDTO:
        payload = {
            **self.validated_data,
            "command_id": str(self.validated_data["command_id"]),
        }
        return GetCommandInputDTO(**payload)

    @staticmethod
    def to_output_dto(command: Command) -> GetCommandOutputDTO:
        payload = command_to_output(command)
        return GetCommandOutputDTO(**payload)

    @staticmethod
    def to_response(command: Command) -> dict:
        return command_to_output(command)
