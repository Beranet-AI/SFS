from apps.commands.application.services.commands_service import CommandsService
from apps.commands.application.services.discovery_result_service import (
    DiscoveryResultService,
)
from apps.commands.domain.enums.command_type import CommandType
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
        discovery_result_service: DiscoveryResultService | None = None,
    ) -> None:
        self._service = CommandsService(
            command_repository=command_repository,
            attempt_repository=attempt_repository,
        )
        self._command_repository = command_repository
        self._discovery_result_service = discovery_result_service

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

        if not self._discovery_result_service:
            return

        command = self._command_repository.get(command_id=dto.command_id)
        if command.command_name != CommandType.DISCOVER.value:
            return

        result_payload = dict(dto.result or {})
        if "devices" not in result_payload and dto.meta:
            if isinstance(dto.meta.get("devices"), list):
                result_payload["devices"] = dto.meta["devices"]

        self._discovery_result_service.handle_result(
            command_id=dto.command_id,
            status=status,
            result=result_payload,
        )
