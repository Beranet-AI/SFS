from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from backend.services.monitoring.domain.enums import DeviceHealth


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class DeviceHealthState:
    device_id: str
    last_seen_at: datetime
    health: DeviceHealth = DeviceHealth.ONLINE

    def mark_seen(self, at: datetime | None = None) -> None:
        self.last_seen_at = at or utcnow()
        self.health = DeviceHealth.ONLINE

    def evaluate_offline(self, offline_threshold_seconds: int, now: datetime | None = None) -> bool:
        now = now or utcnow()
        delta = (now - self.last_seen_at).total_seconds()
        if delta >= offline_threshold_seconds:
            self.health = DeviceHealth.OFFLINE
            return True
        return False
