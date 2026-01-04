from dataclasses import dataclass


@dataclass
class UpdateUserOutputSchema:
    id: str
    email: str
