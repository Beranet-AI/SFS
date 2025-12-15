# core/entities/user.py
from dataclasses import dataclass
from core.value_objects.identifiers import UUID

@dataclass(frozen=True)
class UserEntity:
    id: UUID
    username: str
    role: str   # admin | vet | operator | viewer
    is_active: bool
