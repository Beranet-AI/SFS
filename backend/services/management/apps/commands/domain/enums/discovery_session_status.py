from enum import Enum


class DiscoverySessionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

    @classmethod
    def from_value(cls, value: str) -> "DiscoverySessionStatus":
        try:
            return cls(value)
        except ValueError:
            return cls.PENDING
