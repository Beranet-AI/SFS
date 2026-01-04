from dataclasses import dataclass


@dataclass
class DeleteUserOutputSchema:
    user_id: str
    deleted: bool
