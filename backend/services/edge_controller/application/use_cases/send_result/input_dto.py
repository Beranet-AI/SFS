from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from ....schemas.result.send_result_input import SendResultInput


@dataclass
class SendResultInputDTO(SendResultInput):
    command_id: str
    command_type: str
    status: str
    executed_at: datetime
    payload: Dict[str, Any]
