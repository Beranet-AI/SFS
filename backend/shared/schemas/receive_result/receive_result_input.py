from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ReceiveResultInput:
    command_id: str
    attempt_no: int
    status: str
    result: Dict[str, Any]
    error_code: str
    error_message: str
    meta: Dict[str, Any]

    def to_dict(self) -> dict:
        return {
            "command_id": self.command_id,
            "attempt_no": self.attempt_no,
            "status": self.status,
            "result": self.result,
            "error_code": self.error_code,
            "error_message": self.error_message,
            "meta": self.meta,
        }
