from abc import ABC, abstractmethod
from apps.telemetry.domain.records.telemetry_record import TelemetryRecord

class TelemetryRepository(ABC):

    @abstractmethod
    def save(self, record: TelemetryRecord) -> None: ...

    @abstractmethod
    def list_recent(self, livestock_id: str, limit: int = 100): ...
