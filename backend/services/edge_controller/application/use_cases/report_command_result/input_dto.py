from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class ReportCommandResultInputDTO:
    command_id: str
    command_type: str
    status: str
    executed_at: datetime
    payload: Dict[str, Any]
