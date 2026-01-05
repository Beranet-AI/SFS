from apps.commands.domain.enums.command_status import CommandStatus
from apps.commands.domain.repositories.command_repository import CommandRepository


class CommandTracker:
    """Track command execution lifecycle."""

    def __init__(self, *, command_repository: CommandRepository) -> None:
        self._command_repository = command_repository

    def acknowledge(
        self,
        *,
        command_id: str,
        attempt_no: int,
        executor_receipt: str | None,
        meta: dict | None,
    ) -> None:
        self._command_repository.record_execution_ack(
            command_id=command_id,
            attempt_no=attempt_no,
            executor_receipt=executor_receipt,
            meta=meta,
        )
        self._command_repository.mark_acked(command_id=command_id, meta=meta)

    def record_result(
        self,
        *,
        command_id: str,
        attempt_no: int,
        status: CommandStatus,
        result: dict | None,
        error_code: str,
        error_message: str,
        meta: dict | None,
    ) -> None:
        self._command_repository.record_execution_result(
            command_id=command_id,
            attempt_no=attempt_no,
            status=status.value,
            result=result,
            error_code=error_code,
            error_message=error_message,
            meta=meta,
        )
        self._command_repository.mark_result(
            command_id=command_id,
            status=status,
            result=result,
            error_code=error_code,
            error_message=error_message,
        )
