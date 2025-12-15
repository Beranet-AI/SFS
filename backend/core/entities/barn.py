# core/entities/barn.py
from dataclasses import dataclass
from typing import Optional
from core.value_objects.identifiers import UUID

@dataclass(frozen=True)
class BarnEntity:
    id: UUID
    farm_id: UUID
    name: str
    capacity: Optional[int]
