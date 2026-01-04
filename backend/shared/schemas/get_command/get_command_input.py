from dataclasses import dataclass


@dataclass
class GetCommandInput:
    command_id: str

    def to_dict(self) -> dict:
        return {"command_id": self.command_id}
