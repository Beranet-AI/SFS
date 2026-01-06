from dataclasses import dataclass
from typing import Any, Dict

from shared.schemas.edge_controller.execute_command.execute_command_input import (
    ExecuteCommandInput,
)


@dataclass
class ExecuteCommandInputDTO(ExecuteCommandInput):
    command_id: str
    command_type: str
    edge_id: str
    issued_at: str
    payload: Dict[str, Any]
