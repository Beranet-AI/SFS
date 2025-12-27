from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class DeviceOfflineEvent:
    device_id: str
    ts: datetime
    last_seen_at: datetime
    reason: str = "heartbeat_timeout"
