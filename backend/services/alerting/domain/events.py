from enum import Enum
from typing import Dict, Any
from pydantic import BaseModel
from datetime import datetime


class AlertSeverity(str, Enum):
    info = "info"
    warning = "warning"
    critical = "critical"


class AlertPayload(BaseModel):
    metric: str
    value: float
    minSafe: float | None = None
    maxSafe: float | None = None
    deviceId: str
    zoneId: str | None = None


class LiveEvent(BaseModel):
    id: str
    type: str              # ALERT_RAISED | ALERT_RESOLVED
    severity: AlertSeverity
    payload: AlertPayload
    timestamp: datetime
