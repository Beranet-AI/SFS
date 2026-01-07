from enum import Enum


class CommandStatus(str, Enum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"

    @classmethod
    def to_management_value(cls, value: str) -> str:
        mapping = {
            cls.COMPLETED.value: "succeeded",
            cls.FAILED.value: "failed",
        }
        return mapping.get(value, value)
