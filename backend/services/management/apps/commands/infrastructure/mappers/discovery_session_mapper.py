from apps.commands.domain.entities.discovery_session import DiscoverySession
from apps.commands.domain.enums.discovery_session_status import (
    DiscoverySessionStatus,
)
from apps.commands.infrastructure.models.discovery_session_model import (
    DiscoverySessionModel,
)


class DiscoverySessionMapper:
    @staticmethod
    def to_domain(model: DiscoverySessionModel) -> DiscoverySession:
        return DiscoverySession(
            id=str(model.id),
            edge_node_id=model.edge_node_id,
            status=DiscoverySessionStatus.from_value(model.status),
            command_id=str(model.command_id) if model.command_id else None,
            started_by=model.started_by,
            started_at=model.started_at,
            finished_at=model.finished_at,
            device_count=model.device_count,
            error_message=model.error_message,
        )
