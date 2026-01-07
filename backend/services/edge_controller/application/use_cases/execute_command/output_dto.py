from dataclasses import dataclass
from typing import Any, Dict, List

from shared.schemas.edge_controller.execute_command.execute_command_output import (
    DiscoverCommandOutput,
    ExecuteCommandOutput,
    OnOffCommandOutput,
    RebootCommandOutput,
)


@dataclass
class BaseCommandResultDTO(ExecuteCommandOutput):
    command_id: str
    command_type: str
    status: str
    executed_at: str


@dataclass
class DiscoverCommandResultDTO(DiscoverCommandOutput, BaseCommandResultDTO):
    scan_id: str
    devices: List[Dict[str, Any]]
    message: str


@dataclass
class OnOffCommandResultDTO(OnOffCommandOutput, BaseCommandResultDTO):
    device_id: str
    execution_state: str


@dataclass
class RebootCommandResultDTO(RebootCommandOutput, BaseCommandResultDTO):
    device_id: str
    reboot_state: str
