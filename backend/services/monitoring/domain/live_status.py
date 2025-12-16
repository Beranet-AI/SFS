from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class LiveStatusSeverity(str, Enum):
    info = "info"
    warning = "warning"
    critical = "critical"


class LiveStatusPayload(BaseModel):
    metric: str
    value: float
    minSafe: float | None = None
    maxSafe: float | None = None
    deviceId: str
    zoneId: str | None = None


class LiveStatusEvent(BaseModel):
    id: str
    type: str  # LIVE_STATUS_RAISED | LIVE_STATUS_RESOLVED
    severity: LiveStatusSeverity
    payload: LiveStatusPayload
    timestamp: datetime
