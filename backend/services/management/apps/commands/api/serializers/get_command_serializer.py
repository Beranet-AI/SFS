from apps.commands.application.use_cases.get_command.input_dto import (
    GetCommandInputDTO,
)
from apps.commands.application.use_cases.get_command.output_dto import (
    GetCommandOutputDTO,
)
from apps.commands.domain.entities.command import Command
from apps.commands.api.serializers.send_command_serializer import _command_to_output


class GetCommandSerializer:
    @staticmethod
    def to_input_dto(data: dict) -> GetCommandInputDTO:
        payload = {**data, "command_id": str(data["command_id"])}
        return GetCommandInputDTO(**payload)

    @staticmethod
    def to_output_dto(command: Command) -> GetCommandOutputDTO:
        payload = _command_to_output(command)
        return GetCommandOutputDTO(**payload)

    @staticmethod
    def to_response(command: Command) -> dict:
        return _command_to_output(command)
