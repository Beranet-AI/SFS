from datetime import datetime
from shared.ids.incident_id import IncidentId
from shared.ids.livestock_id import LivestockId
from shared.enums.incident_severity import IncidentSeverity
from shared.enums.incident_status import IncidentStatus

class IncidentDTO:
    """
    Incident contract shared between backend and frontend.
    """

    def __init__(
        self,
        id: IncidentId,
        livestock_id: LivestockId,
        severity: IncidentSeverity,
        status: IncidentStatus,
        created_at: datetime,
        description: str
    ):
        self.id = id
        self.livestock_id = livestock_id
        self.severity = severity
        self.status = status
        self.created_at = created_at
        self.description = description
