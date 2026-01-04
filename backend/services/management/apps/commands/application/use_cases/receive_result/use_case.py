from apps.commands.application.services.command_lifecycle_service import (
    CommandLifecycleService,
)
from apps.commands.domain.enums.command_status import CommandStatus
from apps.commands.domain.repositories.command_attempt_repository import (
    CommandAttemptRepository,
)
from apps.commands.domain.repositories.command_repository import CommandRepository
from .input_dto import ReceiveResultInputDTO


class ReceiveResultUseCase:
    def __init__(
        self,
        *,
        command_repository: CommandRepository,
        attempt_repository: CommandAttemptRepository,
    ) -> None:
        self._service = CommandLifecycleService(
            command_repository=command_repository,
            attempt_repository=attempt_repository,
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
