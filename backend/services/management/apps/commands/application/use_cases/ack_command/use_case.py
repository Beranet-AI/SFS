from apps.commands.application.services.command_lifecycle_service import (
    CommandLifecycleService,
)
from apps.commands.domain.repositories.command_attempt_repository import (
    CommandAttemptRepository,
)
from apps.commands.domain.repositories.command_repository import CommandRepository
from apps.commands.infrastructure.repositories.command_attempt_repository import (
    DjangoCommandAttemptRepository,
)
from apps.commands.infrastructure.repositories.command_repository import (
    DjangoCommandRepository,
)
from .input_dto import AckCommandInputDTO


class AckCommandUseCase:
    def __init__(
        self,
        *,
        command_repository: CommandRepository | None = None,
        attempt_repository: CommandAttemptRepository | None = None,
    ) -> None:
        repository = command_repository or DjangoCommandRepository()
        attempts = attempt_repository or DjangoCommandAttemptRepository()
        self._service = CommandLifecycleService(
            command_repository=repository,
            attempt_repository=attempts,
        )

    def execute(self, dto: AckCommandInputDTO) -> None:
        self._service.acknowledge(
            command_id=dto.command_id,
            attempt_no=dto.attempt_no,
            executor_receipt=dto.executor_receipt,
            meta=dto.meta,
        )
