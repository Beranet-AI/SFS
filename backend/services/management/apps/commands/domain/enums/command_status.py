from enum import Enum


class CommandStatus(str, Enum):
    PENDING = "pending"
    DISPATCHED = "dispatched"
    ACKED = "acked"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    TIMED_OUT = "timed_out"
    CANCELLED = "cancelled"
    DEAD_LETTERED = "dead_lettered"

    @classmethod
    def from_value(cls, value: str) -> "CommandStatus":
        return cls(value)
