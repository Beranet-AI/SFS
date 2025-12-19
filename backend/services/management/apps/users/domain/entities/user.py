from dataclasses import dataclass
from apps.users.domain.enums.role import Role

@dataclass
class User:
    id: str
    email: str
    role: Role
    is_active: bool = True
