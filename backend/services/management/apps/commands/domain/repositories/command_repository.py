from typing import Protocol

from apps.commands.domain.entities.command import Command
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
