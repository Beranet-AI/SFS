from dataclasses import dataclass
from typing import Any


@dataclass
class ReceiveResultInputDTO:
    command_id: str
    attempt_no: int
    status: str
    result: dict[str, Any] | None = None
    error_code: str = ""
    error_message: str = ""
    meta: dict[str, Any] | None = None
