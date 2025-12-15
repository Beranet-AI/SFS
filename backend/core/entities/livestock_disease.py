# core/entities/livestock_disease.py
from dataclasses import dataclass
from typing import Optional
from core.value_objects.identifiers import UUID
from core.value_objects.timestamps import ISODateString

@dataclass(frozen=True)
class LivestockDiseaseEntity:
    livestock_id: UUID
    disease_id: UUID

    diagnosed_at: ISODateString
    severity: str            # mild / moderate / severe
    notes: Optional[str]
