from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SendCommandInputDTO:
    command_name: str
    target_kind: str
    target_id: str
    payload: dict[str, Any] | None = None

    # optional metadata
    idempotency_key: str = ""
    source: str = "manual"
    created_by: str = ""
    ack_deadline_sec: int = 10
    result_deadline_sec: int = 60
    max_attempts: int = 5
