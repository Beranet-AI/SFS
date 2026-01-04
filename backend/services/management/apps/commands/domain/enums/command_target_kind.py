from enum import Enum


class CommandTargetKind(str, Enum):
    DEVICE = "device"
    LIVESTOCK = "livestock"
    LOCATION = "location"

    @classmethod
    def from_value(cls, value: str) -> "CommandTargetKind":
        try:
            return cls(value)
        except ValueError:
            return cls.DEVICE
