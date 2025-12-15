from typing import Iterable

from apps.events.domain.entities import Event
from apps.events.infrastructure.repositories import EventRepository


class EventService:
    def __init__(self, repo: EventRepository | None = None):
        self.repo = repo or EventRepository()

    def list_events(self) -> Iterable[Event]:
        return self.repo.list_active()

    def acknowledge(self, event_id: str) -> Event:
        return self.repo.ack(event_id)

    def resolve(self, event_id: str) -> Event:
        return self.repo.resolve(event_id)
