# core/entities/farm.py
from dataclasses import dataclass
from core.value_objects.identifiers import UUID
from core.value_objects.timestamps import ISODateString

@dataclass(frozen=True)
class FarmEntity:
    id: UUID
    name: str
    location: str

    created_at: ISODateString
