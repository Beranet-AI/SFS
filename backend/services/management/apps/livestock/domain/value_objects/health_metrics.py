# File: livestock/domain/value_objects/health_metrics.py
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class HealthMetrics:
    temperature_c: float
    activity: float
    rumination_minutes: Optional[float] = None
    movement_index: Optional[float] = None
    lying_minutes: Optional[float] = None
    standing_minutes: Optional[float] = None
    heart_rate_bpm: Optional[int] = None
