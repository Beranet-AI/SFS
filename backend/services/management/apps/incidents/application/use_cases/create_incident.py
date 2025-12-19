from datetime import datetime
from apps.incidents.domain.entities.incident import Incident
from apps.incidents.domain.enums.incident_status import IncidentStatus

class CreateIncidentUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(
        self,
        incident_id,
        livestock_id,
        severity,
        source,
        description: str,
    ):
        incident = Incident(
            id=incident_id,
            livestock_id=livestock_id,
            severity=severity,
            status=IncidentStatus.OPEN,
            source=source,
            description=description,
            created_at=datetime.utcnow(),
        )
        self.repo.save(incident)
        return incident
