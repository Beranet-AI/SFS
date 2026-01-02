# File: livestock/application/use_cases/record_health_metrics/input_dto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class RecordHealthMetricsInputDTO:
    livestock_id: str
    temperature_c: float
    activity: float
    rumination_minutes: Optional[float] = None
    movement_index: Optional[float] = None
    lying_minutes: Optional[float] = None
    standing_minutes: Optional[float] = None
    heart_rate_bpm: Optional[int] = None
