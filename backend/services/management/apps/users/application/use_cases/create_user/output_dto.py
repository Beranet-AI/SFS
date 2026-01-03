from dataclasses import dataclass


@dataclass
class CreateUserOutputDTO:
    id: str
    email: str
