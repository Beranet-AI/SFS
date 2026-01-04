from apps.commands.domain.repositories.command_repository import CommandRepository
from apps.commands.infrastructure.repositories.command_repository import (
    DjangoCommandRepository,
)
from .input_dto import GetCommandInputDTO


class GetCommandUseCase:
    def __init__(self, repository: CommandRepository | None = None) -> None:
        self._repository = repository or DjangoCommandRepository()

    def execute(self, dto: GetCommandInputDTO):
        return self._repository.get(command_id=dto.command_id)
