from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class CommandExecution:
    id: str
    command_id: str
    attempt_no: int
    status: str
    created_at: datetime
    dispatched_at: datetime | None = None
    acked_at: datetime | None = None
    result_at: datetime | None = None
    executor_receipt: str = ""
    debug: dict[str, Any] | None = None
