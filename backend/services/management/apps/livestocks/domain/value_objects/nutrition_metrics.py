# File: livestock/domain/value_objects/nutrition_metrics.py
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class NutritionMetrics:
    feed_intake_kg: float
    water_intake_l: float
    feeder_station_id: Optional[str] = None
