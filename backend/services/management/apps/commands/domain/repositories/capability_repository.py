from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class CommandCapability:
    device_category: str
    device_type: str
    command_category: str
    command_type: str
    adapter_type: str


class CapabilityRepository(Protocol):
    def list_capabilities(self) -> list[CommandCapability]:
        ...
