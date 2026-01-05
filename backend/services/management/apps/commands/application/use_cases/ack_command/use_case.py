from apps.commands.application.services.commands_service import CommandsService
from apps.commands.domain.repositories.command_attempt_repository import (
    CommandAttemptRepository,
)
from apps.commands.domain.repositories.command_repository import CommandRepository
from .input_dto import AckCommandInputDTO


class AckCommandUseCase:
    def __init__(
        self,
        *,
        command_repository: CommandRepository,
        attempt_repository: CommandAttemptRepository,
    ) -> None:
        self._service = CommandsService(
            command_repository=command_repository,
            attempt_repository=attempt_repository,
        )

    def execute(self, dto: AckCommandInputDTO) -> None:
        self._service.acknowledge(
            command_id=dto.command_id,
            attempt_no=dto.attempt_no,
            executor_receipt=dto.executor_receipt,
            meta=dto.meta,
        )
