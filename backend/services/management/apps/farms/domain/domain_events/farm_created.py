from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class FarmCreated:
    farm_id: str
    name: str
    occurred_at: datetime
