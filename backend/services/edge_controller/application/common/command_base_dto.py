from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class CommandBaseDTO:
    command_id: str
    command_type: str
    edge_id: str
    issued_at: datetime
    source: Optional[str] = None
