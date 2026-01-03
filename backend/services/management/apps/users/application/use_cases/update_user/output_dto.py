from dataclasses import dataclass


@dataclass
class UpdateUserOutputDTO:
    id: str
    email: str
