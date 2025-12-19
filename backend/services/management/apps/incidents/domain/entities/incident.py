from dataclasses import dataclass
from datetime import datetime
from shared.ids.incident_id import IncidentId
from shared.ids.livestock_id import LivestockId
from shared.enums.incident_severity import IncidentSeverity
from apps.incidents.domain.enums.incident_status import IncidentStatus
from apps.incidents.domain.enums.incident_source import IncidentSource

@dataclass
class Incident:
    id: IncidentId
    livestock_id: LivestockId
    severity: IncidentSeverity
    status: IncidentStatus
    source: IncidentSource
    description: str
    created_at: datetime
    acknowledged_at: datetime | None = None
    resolved_at: datetime | None = None

    def acknowledge(self, at: datetime):
        if self.status != IncidentStatus.OPEN:
            raise ValueError("Only OPEN incidents can be acknowledged")
        self.status = IncidentStatus.ACKNOWLEDGED
        self.acknowledged_at = at

    def resolve(self, at: datetime):
        if self.status not in (
            IncidentStatus.OPEN,
            IncidentStatus.ACKNOWLEDGED,
        ):
            raise ValueError("Incident cannot be resolved")
        self.status = IncidentStatus.RESOLVED
        self.resolved_at = at
