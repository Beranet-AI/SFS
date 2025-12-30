from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


from ......shared.schemas.edge_controller.command.execute_command_output import (
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
    executed_at: datetime


@dataclass
class DiscoverCommandResultDTO(DiscoverCommandOutput, BaseCommandResultDTO):
    devices: List[Dict[str, Any]]


@dataclass
class OnOffCommandResultDTO(OnOffCommandOutput, BaseCommandResultDTO):
    device_id: str
    execution_state: str


@dataclass
class RebootCommandResultDTO(RebootCommandOutput, BaseCommandResultDTO):
    device_id: str
    reboot_state: str
