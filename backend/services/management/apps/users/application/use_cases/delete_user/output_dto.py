from dataclasses import dataclass


@dataclass
class DeleteUserOutputDTO:
    user_id: str
    deleted: bool
