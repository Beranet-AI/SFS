from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any


@dataclass
class BaseCommandResultDTO:
    command_id: str
    command_type: str
    status: str
    executed_at: datetime


@dataclass
class DiscoverCommandResultDTO(BaseCommandResultDTO):
    devices: List[Dict[str, Any]]


@dataclass
class OnOffCommandResultDTO(BaseCommandResultDTO):
    device_id: str
    execution_state: str


@dataclass
class RebootCommandResultDTO(BaseCommandResultDTO):
    device_id: str
    reboot_state: str
