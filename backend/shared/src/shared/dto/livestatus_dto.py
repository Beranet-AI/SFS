from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Dict

@dataclass
class LiveStatusDTO:
    ts: datetime
    device_id: str
    device_type: str
    farm_id: Optional[str]
    barn_id: Optional[str]
    zone_id: Optional[str]
    livestock_id: Optional[str]
    metrics: Dict[str, Any]  # مثل {"temperature": 23.1, "ammonia": 15}
