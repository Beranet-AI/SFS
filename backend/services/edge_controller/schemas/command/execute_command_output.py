from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ExecuteCommandOutput:
    command_id: str
    command_type: str
    status: str
    executed_at: str


@dataclass
class DiscoverCommandOutput(ExecuteCommandOutput):
    devices: List[Dict[str, Any]]


@dataclass
class OnOffCommandOutput(ExecuteCommandOutput):
    device_id: str
    execution_state: str


@dataclass
class RebootCommandOutput(ExecuteCommandOutput):
    device_id: str
    reboot_state: str
