from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class CommandResult:
    command_id: str
    status: str
    result: dict[str, Any] | None
    error_code: str = ""
    error_message: str = ""
    received_at: datetime | None = None
