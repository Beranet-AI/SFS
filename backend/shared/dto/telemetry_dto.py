from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

@dataclass
class TelemetryDTO:
    device_id: str
    device_type: str
    metric: str
    value: Any
    ts: datetime
    farm_id: Optional[str] = None
    barn_id: Optional[str] = None
    zone_id: Optional[str] = None
    livestock_id: Optional[str] = None
