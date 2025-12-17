from apps.incidents.domain.entities import Incident
from apps.incidents.models import IncidentModel


def orm_to_domain(incident: IncidentModel) -> Incident:
    return Incident(
        id=incident.id,
        severity=incident.severity,
        status=incident.status,
        title=incident.title,
        message=incident.message,
        metric=incident.metric,
        value=incident.value,
        farm_id=incident.farm_id,
        barn_id=incident.barn_id,
        zone_id=incident.zone_id,
        device_id=incident.device_id,
        created_at=incident.created_at,
        updated_at=incident.updated_at,
    )


def domain_to_orm(incident: Incident) -> IncidentModel:
    return IncidentModel(
        id=incident.id,
        severity=incident.severity,
        status=incident.status,
        title=incident.title,
        message=incident.message,
        metric=incident.metric,
        value=incident.value,
        farm_id=incident.farm_id,
        barn_id=incident.barn_id,
        zone_id=incident.zone_id,
        device_id=incident.device_id,
    )
