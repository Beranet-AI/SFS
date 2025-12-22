from datetime import datetime
from shared.enums.health_state import HealthState

class HealthStatusDTO:
    """
    Current evaluated health status of a livestock.
    """

    def __init__(
        self,
        state: HealthState,
        confidence: float,
        evaluated_at: datetime
    ):
        self.state = state
        self.confidence = confidence
        self.evaluated_at = evaluated_at
