from dataclasses import dataclass
from typing import Any, Dict

from shared.schemas.management.commands.ack_command.ack_command_input import AckCommandInput


@dataclass
class AckCommandInputDTO(AckCommandInput):
    command_id: str
    attempt_no: int
    executor_receipt: str | None = None
    meta: Dict[str, Any] | None = None
