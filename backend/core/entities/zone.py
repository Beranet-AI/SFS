# core/entities/zone.py
from dataclasses import dataclass
from core.value_objects.identifiers import UUID

@dataclass(frozen=True)
class ZoneEntity:
    id: UUID
    barn_id: UUID
    name: str
