from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SendCommandOutputDTO:
    command_id: str
    status: str
    last_result: dict[str, Any] | None = None
