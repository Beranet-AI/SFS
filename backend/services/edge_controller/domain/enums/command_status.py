from enum import Enum


class CommandStatus(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
