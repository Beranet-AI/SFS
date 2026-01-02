from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class HealthSnapshot:
    status: str
    temperature: float
    recorded_at: datetime
