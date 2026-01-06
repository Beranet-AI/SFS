from apps.commands.domain.repositories.command_repository import CommandRepository

from .input_dto import GetCommandInputDTO
from .output_dto import GetCommandOutputDTO


class GetCommandUseCase:
    def __init__(self, *, command_repository: CommandRepository) -> None:
        self._command_repository = command_repository

    def execute(self, dto: GetCommandInputDTO) -> GetCommandOutputDTO:
        if not dto.command_id:
            raise ValueError("command_id is required")
        command = self._command_repository.get(command_id=dto.command_id)
        return GetCommandOutputDTO(command=command)
