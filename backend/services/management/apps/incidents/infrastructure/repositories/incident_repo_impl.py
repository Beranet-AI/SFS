from apps.incidents.domain.entities.incident import Incident
from apps.incidents.infrastructure.models.incident_model import IncidentModel
from apps.incidents.domain.enums.incident_status import IncidentStatus
from apps.incidents.domain.enums.incident_source import IncidentSource
from shared.ids.incident_id import IncidentId
from shared.ids.livestock_id import LivestockId
from shared.enums.incident_severity import IncidentSeverity

class DjangoIncidentRepository:

    def get_by_id(self, incident_id: IncidentId) -> Incident:
        obj = IncidentModel.objects.get(id=str(incident_id))
        return Incident(
            id=IncidentId(str(obj.id)),
            livestock_id=LivestockId(obj.livestock_id),
            severity=IncidentSeverity(obj.severity),
            status=IncidentStatus(obj.status),
            source=IncidentSource(obj.source),
            description=obj.description,
            created_at=obj.created_at,
            acknowledged_at=obj.acknowledged_at,
            resolved_at=obj.resolved_at,
        )

    def save(self, incident: Incident) -> None:
        IncidentModel.objects.update_or_create(
            id=str(incident.id),
            defaults={
                "livestock_id": str(incident.livestock_id),
                "severity": incident.severity.value,
                "status": incident.status.value,
                "source": incident.source.value,
                "description": incident.description,
                "created_at": incident.created_at,
                "acknowledged_at": incident.acknowledged_at,
                "resolved_at": incident.resolved_at,
            },
        )
