from typing import Protocol

from apps.commands.domain.repositories.capability_repository import CapabilityRepository
from apps.commands.domain.specifications.is_edge_command import IsEdgeCommand


class CommandExecutor(Protocol):
    def execute(self, *, edge_id: str, command: dict) -> None:
        ...


class CommandDispatcher:
    def __init__(
        self,
        *,
        edge_executor: CommandExecutor,
        device_executor: CommandExecutor,
        capability_repository: CapabilityRepository,
    ) -> None:
        self._edge_executor = edge_executor
        self._device_executor = device_executor
        self._is_edge_command = IsEdgeCommand(
            capability_repository=capability_repository
        )

    def dispatch(
        self,
        *,
        command: dict,
        edge_id: str,
        device_category: str | None,
        device_type: str | None,
        command_type: str,
    ) -> None:
        if self._is_edge_command(
            device_category=device_category,
            device_type=device_type,
            command_type=command_type,
        ):
            self._edge_executor.execute(edge_id=edge_id, command=command)
            return

        self._device_executor.execute(edge_id=edge_id, command=command)
