from dataclasses import dataclass
from datetime import datetime
from shared.ids.livestock_id import LivestockId
from apps.health.domain.enums.diagnosis_type import DiagnosisType

@dataclass
class MedicalRecord:
    id: str
    livestock_id: LivestockId
    diagnosis: DiagnosisType
    notes: str
    recorded_at: datetime
