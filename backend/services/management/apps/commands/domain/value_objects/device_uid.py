from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceUid:
    value: str
