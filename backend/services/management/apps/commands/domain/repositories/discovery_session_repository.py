from typing import Protocol

from apps.commands.domain.entities.discovery_session import DiscoverySession


class DiscoverySessionRepository(Protocol):
    def create(self, *, edge_node_id: str, started_by: str) -> DiscoverySession:
        ...

    def get(self, *, session_id: str) -> DiscoverySession:
        ...

    def get_by_command_id(self, *, command_id: str) -> DiscoverySession | None:
        ...

    def attach_command(self, *, session_id: str, command_id: str) -> DiscoverySession:
        ...

    def mark_running(self, *, session_id: str) -> DiscoverySession:
        ...

    def mark_completed(
        self, *, session_id: str, device_count: int
    ) -> DiscoverySession:
        ...

    def mark_failed(
        self, *, session_id: str, error_message: str
    ) -> DiscoverySession:
        ...
