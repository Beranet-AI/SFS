# File: livestock/application/use_cases/record_nutrition_metrics/output_dto.py
from dataclasses import dataclass

@dataclass
class RecordNutritionMetricsOutputDTO:
    livestock_id: str
