from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class LiveStatusEvent:
    device_id: str
    ts: datetime
    metric: str
    value: float
    unit: str | None = None
    meta: dict[str, Any] | None = None
