from apps.commands.domain.repositories.command_repository import CommandRepository
from .input_dto import GetCommandInputDTO


class GetCommandUseCase:
    def __init__(self, repository: CommandRepository) -> None:
        self._repository = repository

    def execute(self, dto: GetCommandInputDTO):
        return self._repository.get(command_id=dto.command_id)
