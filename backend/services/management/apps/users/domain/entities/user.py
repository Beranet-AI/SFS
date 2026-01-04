from dataclasses import dataclass

from apps.users.domain.value_objects.email import Email


@dataclass
class User:
    id: str | None
    email: Email
    phone_number: str
    is_staff: bool
    is_superuser: bool
    is_active: bool
    is_active_account: bool
