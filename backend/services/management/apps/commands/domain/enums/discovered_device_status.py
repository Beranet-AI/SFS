from enum import Enum


class DiscoveredDeviceStatus(str, Enum):
    NEW = "new"
    REGISTERED = "registered"

    @classmethod
    def from_value(cls, value: str) -> "DiscoveredDeviceStatus":
        try:
            return cls(value)
        except ValueError:
            return cls.NEW
