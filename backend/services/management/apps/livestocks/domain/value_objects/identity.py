# File: livestock/domain/value_objects/identity.py
'''
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class LivestockIdentity:
    tag_id: str
    breed: str
    birth_date: Optional[date]
    sex: str  # "MALE" | "FEMALE"
    herd_entry_date: Optional[date]
    status: str  # "ACTIVE" | "INACTIVE" | "CULLED" | "DELETED"
'''

from dataclasses import dataclass

@dataclass(frozen=True)
class Identity:
    tag_id: str
    species: str
    breed: str
