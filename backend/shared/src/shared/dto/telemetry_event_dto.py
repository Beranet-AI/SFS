from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime


@dataclass(frozen=True)
class TelemetryEventDTO:
    """
    Generic telemetry/event envelope (industrial friendly).
    """
    device_serial: str
    device_type: str
    metric: str                # e.g. temperature_c, humidity_pct, fan_rpm
    value: float
    unit: Optional[str] = None

    ts: datetime = field(default_factory=datetime.utcnow)

    # optional routing/assignment info
    farm_id: Optional[str] = None
    barn_id: Optional[str] = None
    zone_id: Optional[str] = None
    livestock_id: Optional[str] = None

    # raw payload for traceability
    raw: Dict[str, Any] = field(default_factory=dict)
