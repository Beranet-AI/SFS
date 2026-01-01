from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class BarnAdded:
    farm_id: str
    barn_id: str
    barn_name: str
    occurred_at: datetime
