from datetime import datetime
from shared.enums.health_state import HealthState
from apps.livestock.domain.value_objects.health_status import HealthStatus

class HealthRules:
    @staticmethod
    def from_score(score: float) -> HealthStatus:
        if score >= 0.85:
            state = HealthState.HEALTHY
        elif score >= 0.65:
            state = HealthState.AT_RISK
        elif score >= 0.40:
            state = HealthState.SICK
        else:
            state = HealthState.CRITICAL

        return HealthStatus(state=state, confidence=score, evaluated_at=datetime.utcnow())
