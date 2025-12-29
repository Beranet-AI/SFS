from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ExecuteCommandInputDTO:
    command_id: str
    command_type: str
    edge_id: str
    issued_at: str
    payload: Dict[str, Any]
