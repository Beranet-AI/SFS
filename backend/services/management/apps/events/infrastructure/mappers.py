from apps.events.domain.entities import Event
from apps.events.infrastructure.orm_models import EventModel


def orm_to_domain(event: EventModel) -> Event:
    return Event(
        id=event.id,
        severity=event.severity,
        status=event.status,
        title=event.title,
        message=event.message,
        metric=event.metric,
        value=event.value,
        farm_id=event.farm_id,
        barn_id=event.barn_id,
        zone_id=event.zone_id,
        device_id=event.device_id,
        created_at=event.created_at,
        updated_at=event.updated_at,
    )


def domain_to_orm(event: Event) -> EventModel:
    return EventModel(
        id=event.id,
        severity=event.severity,
        status=event.status,
        title=event.title,
        message=event.message,
        metric=event.metric,
        value=event.value,
        farm_id=event.farm_id,
        barn_id=event.barn_id,
        zone_id=event.zone_id,
        device_id=event.device_id,
    )
