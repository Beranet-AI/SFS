from dataclasses import dataclass


@dataclass
class DeleteUserInputSchema:
    user_id: str
