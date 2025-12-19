from enum import Enum

class HealthState(str, Enum):
    HEALTHY = "healthy"
    AT_RISK = "at_risk"
    SICK = "sick"
    CRITICAL = "critical"
