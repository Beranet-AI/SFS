from dataclasses import dataclass

@dataclass(frozen=True)
class DeviceId:
    value: str
    def __str__(self) -> str:
        return self.value
