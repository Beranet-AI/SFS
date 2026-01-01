from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ZoneAdded:
    farm_id: str
    barn_id: str
    zone_id: str
    zone_name: str
    occurred_at: datetime
