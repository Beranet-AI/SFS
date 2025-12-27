from dataclasses import dataclass
from datetime import datetime
from backend.shared.enums.health_state import HealthState

@dataclass(frozen=True)
class HealthStatus:
    state: HealthState
    confidence: float
    evaluated_at: datetime
