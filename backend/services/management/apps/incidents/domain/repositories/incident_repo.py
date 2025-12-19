from abc import ABC, abstractmethod
from apps.incidents.domain.entities.incident import Incident
from shared.ids.incident_id import IncidentId

class IncidentRepository(ABC):

    @abstractmethod
    def get_by_id(self, incident_id: IncidentId) -> Incident: ...

    @abstractmethod
    def save(self, incident: Incident) -> None: ...
