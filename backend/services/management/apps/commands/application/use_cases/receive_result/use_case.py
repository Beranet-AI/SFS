from apps.commands.application.services.command_lifecycle_service import (
    CommandLifecycleService,
)
from apps.commands.domain.enums.command_status import CommandStatus
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
from .input_dto import ReceiveResultInputDTO


class ReceiveResultUseCase:
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

    def execute(self, dto: ReceiveResultInputDTO) -> None:
        status = CommandStatus.from_value(dto.status)
        self._service.record_result(
            command_id=dto.command_id,
            attempt_no=dto.attempt_no,
            status=status,
            result=dto.result,
            error_code=dto.error_code,
            error_message=dto.error_message,
            meta=dto.meta,
        )
