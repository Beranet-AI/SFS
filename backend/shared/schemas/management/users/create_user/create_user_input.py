from dataclasses import dataclass


@dataclass
class CreateUserInputSchema:
    email: str
    password: str
    phone_number: str
    is_staff: bool
    is_superuser: bool
