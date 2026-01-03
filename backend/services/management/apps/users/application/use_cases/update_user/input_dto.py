from dataclasses import dataclass


@dataclass
class UpdateUserInputDTO:
    user_id: str
    email: str | None = None
    phone_number: str | None = None
    is_active: bool | None = None
