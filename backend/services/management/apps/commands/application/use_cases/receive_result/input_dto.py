from dataclasses import dataclass
from typing import Any, Dict


from backend.shared.schemas.management.commands.result.receive_result_input import ReceiveResultInput

@dataclass
class ReceiveResultInputDTO(ReceiveResultInput):
    command_id: str
    attempt_no: int
    status: str
    result: Dict[str, Any]
    error_code: str
    error_message: str
    meta: Dict[str, Any]
