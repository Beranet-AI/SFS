from dataclasses import dataclass
from datetime import datetime

from apps.commands.domain.enums.discovery_session_status import (
    DiscoverySessionStatus,
)


@dataclass(frozen=True)
class DiscoverySession:
    id: str
    edge_node_id: str
    status: DiscoverySessionStatus
    command_id: str | None
    started_by: str
    started_at: datetime
    finished_at: datetime | None
    device_count: int
    error_message: str
