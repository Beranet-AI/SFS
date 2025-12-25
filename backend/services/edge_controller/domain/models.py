from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

@dataclass
class DiscoveredDevice:
    external_id: str
    name: str
    device_type: str
    protocol: str
    role: str  # sensor/actuator
    ip: Optional[str]
    meta: Dict[str, Any]
    last_seen: datetime

@dataclass
class TelemetryPacket:
    device_external_id: str
    device_type: str
    metric: str
    value: Any
    ts: datetime
    farm_id: Optional[str] = None
    barn_id: Optional[str] = None
    zone_id: Optional[str] = None
    livestock_id: Optional[str] = None
