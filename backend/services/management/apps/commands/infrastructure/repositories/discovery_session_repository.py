from apps.commands.domain.entities.discovery_session import DiscoverySession
from apps.commands.domain.repositories.discovery_session_repository import (
    DiscoverySessionRepository,
)
from apps.commands.infrastructure.mappers.discovery_session_mapper import (
    DiscoverySessionMapper,
)
from apps.commands.infrastructure.models.discovery_session_model import (
    DiscoverySessionModel,
)


class DjangoDiscoverySessionRepository(DiscoverySessionRepository):
    def create(self, *, edge_node_id: str, started_by: str) -> DiscoverySession:
        session = DiscoverySessionModel.objects.create(
            edge_node_id=edge_node_id,
            started_by=started_by or "",
        )
        return DiscoverySessionMapper.to_domain(session)

    def get(self, *, session_id: str) -> DiscoverySession:
        session = DiscoverySessionModel.objects.get(id=session_id)
        return DiscoverySessionMapper.to_domain(session)

    def get_by_command_id(self, *, command_id: str) -> DiscoverySession | None:
        session = (
            DiscoverySessionModel.objects.filter(command_id=command_id)
            .order_by("-started_at")
            .first()
        )
        if not session:
            return None
        return DiscoverySessionMapper.to_domain(session)

    def attach_command(self, *, session_id: str, command_id: str) -> DiscoverySession:
        session = DiscoverySessionModel.objects.get(id=session_id)
        session.command_id = command_id
        session.save(update_fields=["command_id"])
        return DiscoverySessionMapper.to_domain(session)

    def mark_running(self, *, session_id: str) -> DiscoverySession:
        session = DiscoverySessionModel.objects.get(id=session_id)
        session.mark_running()
        return DiscoverySessionMapper.to_domain(session)

    def mark_completed(
        self, *, session_id: str, device_count: int
    ) -> DiscoverySession:
        session = DiscoverySessionModel.objects.get(id=session_id)
        session.mark_completed(device_count=device_count)
        return DiscoverySessionMapper.to_domain(session)

    def mark_failed(
        self, *, session_id: str, error_message: str
    ) -> DiscoverySession:
        session = DiscoverySessionModel.objects.get(id=session_id)
        session.mark_failed(error_message=error_message)
        return DiscoverySessionMapper.to_domain(session)
