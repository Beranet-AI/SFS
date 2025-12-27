from abc import ABC, abstractmethod
from typing import List
from apps.health.domain.entities.medical_record import MedicalRecord


class MedicalRecordRepository(ABC):

    @abstractmethod
    def list_by_livestock(self, livestock_id: str) -> List[MedicalRecord]:
        pass

    @abstractmethod
    def save(self, record: MedicalRecord) -> MedicalRecord:
        pass
