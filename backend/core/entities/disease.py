# core/entities/disease.py
from dataclasses import dataclass
from typing import Optional
from core.value_objects.identifiers import UUID

@dataclass(frozen=True)
class DiseaseEntity:
    id: UUID
    name: str
    code: Optional[str]        # ISO / Vet code
    description: Optional[str]
