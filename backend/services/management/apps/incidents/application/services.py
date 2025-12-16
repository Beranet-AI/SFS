from typing import Iterable

from apps.incidents.domain.entities import Incident
from apps.incidents.infrastructure.repositories import IncidentRepository


class IncidentService:
    def __init__(self, repo: IncidentRepository | None = None):
        self.repo = repo or IncidentRepository()

    def list_incidents(self) -> Iterable[Incident]:
        return self.repo.list_active()

    def create(self, payload: dict) -> Incident:
        return self.repo.create(**payload)

    def acknowledge(self, incident_id: str) -> Incident:
        return self.repo.ack(incident_id)

    def resolve(self, incident_id: str) -> Incident:
        return self.repo.resolve(incident_id)
