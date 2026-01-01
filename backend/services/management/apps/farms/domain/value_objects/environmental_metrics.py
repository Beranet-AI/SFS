# File: farm/domain/value_objects/environmental_metrics.py
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class EnvironmentalMetrics:
    temperature_c: float
    humidity: float
    ammonia_ppm: float
    co2_ppm: Optional[float] = None
    airflow_mps: Optional[float] = None
