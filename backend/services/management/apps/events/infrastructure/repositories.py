from typing import Iterable
from django.utils.timezone import now

from apps.events.domain.entities import Event
from apps.events.domain.enums import EventStatus
from .orm_models import EventModel


class EventRepository:
    @staticmethod
    def to_entity(model: EventModel) -> Event:
        return Event(
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

    def list_active(self) -> Iterable[Event]:
        qs = EventModel.objects.exclude(status=EventStatus.RESOLVED)
        return [self.to_entity(m) for m in qs]

    def get(self, event_id: str) -> Event:
        model = EventModel.objects.get(id=event_id)
        return self.to_entity(model)

    def ack(self, event_id: str) -> Event:
        model = EventModel.objects.get(id=event_id)
        model.status = EventStatus.ACK
        model.updated_at = now()
        model.save(update_fields=["status", "updated_at"])
        return self.to_entity(model)

    def resolve(self, event_id: str) -> Event:
        model = EventModel.objects.get(id=event_id)
        model.status = EventStatus.RESOLVED
        model.updated_at = now()
        model.save(update_fields=["status", "updated_at"])
        return self.to_entity(model)
