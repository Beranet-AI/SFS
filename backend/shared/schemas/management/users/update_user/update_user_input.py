from dataclasses import dataclass


@dataclass
class UpdateUserInputSchema:
    user_id: str
    email: str | None
    phone_number: str | None
    is_active: bool | None
    is_active_account: bool | None
    is_staff: bool | None
    is_superuser: bool | None
