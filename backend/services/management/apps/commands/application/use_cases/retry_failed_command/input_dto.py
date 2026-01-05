from dataclasses import dataclass


@dataclass
class RetryFailedCommandInputDTO:
    command_id: str
