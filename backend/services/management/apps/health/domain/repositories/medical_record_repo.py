from abc import ABC, abstractmethod
from apps.health.domain.entities.medical_record import MedicalRecord
from shared.ids.livestock_id import LivestockId

class MedicalRecordRepository(ABC):

    @abstractmethod
    def add(self, record: MedicalRecord) -> MedicalRecord: ...

    @abstractmethod
    def list_by_livestock(self, livestock_id: LivestockId): ...
