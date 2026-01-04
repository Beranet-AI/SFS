from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass(frozen=True)
class CommandSent:
    command_id: str
    command_name: str
    target_kind: str
    target_id: str
    payload: Dict[str, Any]
    occurred_at: datetime
