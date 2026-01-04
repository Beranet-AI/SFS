from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AckCommandInput:
    command_id: str
    attempt_no: int
    executor_receipt: str | None = None
    meta: Dict[str, Any] | None = None

    def to_dict(self) -> dict:
        data = {
            "command_id": self.command_id,
            "attempt_no": self.attempt_no,
            "executor_receipt": self.executor_receipt,
            "meta": self.meta,
        }
        return {key: value for key, value in data.items() if value is not None}
