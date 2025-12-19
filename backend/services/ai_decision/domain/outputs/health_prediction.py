from dataclasses import dataclass
from datetime import datetime
from shared.enums.health_state import HealthState

@dataclass(frozen=True)
class HealthPrediction:
    """
    Output of AI/ML inference.
    """
    livestock_id: str
    score: float
    state: HealthState
    predicted_at: datetime
