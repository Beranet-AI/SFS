from dataclasses import dataclass
from datetime import datetime
from .enums import EventSeverity, EventStatus


@dataclass(frozen=True)
class Event:
    id: str
    severity: EventSeverity
    status: EventStatus

    title: str
    message: str

    metric: str | None
    value: float | None

    farm_id: str
    barn_id: str | None
    zone_id: str | None
    device_id: str | None

    created_at: datetime
    updated_at: datetime | None
