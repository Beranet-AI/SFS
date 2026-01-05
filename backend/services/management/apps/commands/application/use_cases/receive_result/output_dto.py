from dataclasses import dataclass


@dataclass
class ReceiveResultOutputDTO:
    command_id: str
    status: str
