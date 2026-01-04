from dataclasses import dataclass


@dataclass
class CreateUserOutputSchema:
    id: str
    email: str
