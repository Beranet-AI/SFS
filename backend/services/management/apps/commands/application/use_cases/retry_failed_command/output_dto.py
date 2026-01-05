from dataclasses import dataclass


@dataclass
class RetryFailedCommandOutputDTO:
    command_id: str
    status: str
