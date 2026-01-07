from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SendResultInput:
    command_id: str
    command_type: str
    status: str
    executed_at: str
    payload: Dict[str, Any]
    meta: Dict[str, Any]
