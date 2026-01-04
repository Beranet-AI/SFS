from apps.commands.domain.repositories.command_repository import CommandRepository
from apps.commands.infrastructure.repositories.command_repository import (
    DjangoCommandRepository,
)
from .input_dto import SendCommandInputDTO


class SendCommandUseCase:
    def __init__(self, repository: CommandRepository | None = None) -> None:
        self._repository = repository or DjangoCommandRepository()

    def execute(self, dto: SendCommandInputDTO, *, created_by: str):
        return self._repository.create(data=dto.to_dict(), created_by=created_by)
