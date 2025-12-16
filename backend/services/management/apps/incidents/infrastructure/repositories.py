from typing import Iterable

from django.utils.timezone import now

from apps.incidents.domain.entities import Incident
from apps.incidents.domain.enums import IncidentStatus
from apps.incidents.models import IncidentModel


class IncidentRepository:
    @staticmethod
    def to_entity(model: IncidentModel) -> Incident:
        return Incident(
            id=str(model.id),
            severity=model.severity,
            status=model.status,
            title=model.title,
            message=model.message,
            metric=model.metric,
            value=model.value,
            farm_id=str(model.farm_id),
            barn_id=str(model.barn_id) if model.barn_id else None,
            zone_id=str(model.zone_id) if model.zone_id else None,
            device_id=str(model.device_id) if model.device_id else None,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def list_active(self) -> Iterable[Incident]:
        qs = IncidentModel.objects.exclude(status=IncidentStatus.RESOLVED)
        return [self.to_entity(m) for m in qs]

    def create(
        self,
        *,
        severity: str,
        status: str,
        title: str,
        message: str,
        farm_id: str,
        metric: str | None = None,
        value: float | None = None,
        barn_id: str | None = None,
        zone_id: str | None = None,
        device_id: str | None = None,
    ) -> Incident:
        model = IncidentModel.objects.create(
            severity=severity,
            status=status or IncidentStatus.RAISED,
            title=title,
            message=message,
            metric=metric,
            value=value,
            farm_id=farm_id,
            barn_id=barn_id,
            zone_id=zone_id,
            device_id=device_id,
        )
        return self.to_entity(model)

    def get(self, incident_id: str) -> Incident:
        model = IncidentModel.objects.get(id=incident_id)
        return self.to_entity(model)

    def ack(self, incident_id: str) -> Incident:
        model = IncidentModel.objects.get(id=incident_id)
        model.status = IncidentStatus.ACK
        model.updated_at = now()
        model.save(update_fields=["status", "updated_at"])
        return self.to_entity(model)

    def resolve(self, incident_id: str) -> Incident:
        model = IncidentModel.objects.get(id=incident_id)
        model.status = IncidentStatus.RESOLVED
        model.updated_at = now()
        model.save(update_fields=["status", "updated_at"])
        return self.to_entity(model)
