from dataclasses import dataclass


@dataclass
class CreateUserInputDTO:
    email: str
    password: str
    phone_number: str = ""
    is_staff: bool = False
    is_superuser: bool = False
