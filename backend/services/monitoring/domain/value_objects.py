from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Seconds:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Seconds must be > 0")


@dataclass(frozen=True)
class DeviceId:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("DeviceId cannot be empty")
