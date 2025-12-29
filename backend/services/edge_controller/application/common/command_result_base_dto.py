from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CommandResultBaseDTO:
    command_id: str
    edge_id: str
    command_type: str
    status: str
    executed_at: datetime
    message: Optional[str] = None
