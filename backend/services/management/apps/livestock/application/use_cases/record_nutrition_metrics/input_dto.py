# File: livestock/application/use_cases/record_nutrition_metrics/input_dto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class RecordNutritionMetricsInputDTO:
    livestock_id: str
    feed_intake_kg: float
    water_intake_l: float
    feeder_station_id: Optional[str] = None
