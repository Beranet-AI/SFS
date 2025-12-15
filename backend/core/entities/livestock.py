# core/entities/livestock.py
from dataclasses import dataclass
from typing import Optional
from core.value_objects.identifiers import UUID
from core.value_objects.timestamps import ISODateString

@dataclass(frozen=True)
class LivestockEntity:
    id: UUID

    tag_id: str              # RFID / Ear Tag
    species: str             # cow, sheep, goat
    breed: Optional[str]

    birth_date: Optional[ISODateString]

    farm_id: UUID
    barn_id: UUID
    zone_id: Optional[UUID]

    is_active: bool
