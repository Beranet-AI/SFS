from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ExecuteCommandInput:
    command_id: str
    command_type: str
    edge_id: str
    issued_at: str
    payload: Dict[str, Any]
