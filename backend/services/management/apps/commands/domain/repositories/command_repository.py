from typing import Protocol

from apps.commands.domain.entities.command import Command
from apps.commands.domain.entities.command_execution import CommandExecution
from apps.commands.domain.enums.command_status import CommandStatus


class CommandRepository(Protocol):
    def create(self, *, data: dict, created_by: str) -> Command:
        ...

    def get(self, *, command_id: str) -> Command:
        ...

    def mark_acked(self, *, command_id: str, meta: dict | None = None) -> Command:
        ...

    def mark_dispatched(self, *, command_id: str) -> Command:
        ...

    def mark_result(
        self,
        *,
        command_id: str,
        status: CommandStatus,
        result: dict | None = None,
        error_code: str = "",
        error_message: str = "",
    ) -> Command:
        ...

    def record_execution_ack(
        self,
        *,
        command_id: str,
        attempt_no: int,
        executor_receipt: str | None = None,
        meta: dict | None = None,
    ) -> CommandExecution:
        ...

    def record_execution_result(
        self,
        *,
        command_id: str,
        attempt_no: int,
        status: str,
        result: dict | None = None,
        error_code: str = "",
        error_message: str = "",
        meta: dict | None = None,
    ) -> CommandExecution:
        ...

    def record_scan_result(
        self,
        *,
        scan_id: str,
        device_uid: str,
        payload: dict,
    ) -> None:
        ...
