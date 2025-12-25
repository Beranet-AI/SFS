from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime


@dataclass(frozen=True)
class IncidentDTO:
    """
    Incident created when a rule/policy is violated or device is unhealthy.
    """
    code: str                 # e.g. TEMP_TOO_HIGH, DEVICE_OFFLINE, FAN_FAILURE
    severity: str             # low | medium | high | critical
    title: str
    description: str

    device_serial: Optional[str] = None
    livestock_id: Optional[str] = None
    farm_id: Optional[str] = None
    barn_id: Optional[str] = None
    zone_id: Optional[str] = None

    ts: datetime = field(default_factory=datetime.utcnow)
    evidence: Dict[str, Any] = field(default_factory=dict)
