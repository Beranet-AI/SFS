# File: livestock/application/use_cases/record_nutrition_metrics/use_case.py
from ....domain.value_objects.nutrition_metrics import NutritionMetrics

class RecordNutritionMetricsUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, input_dto):
        livestock = self.repo.get_by_id(input_dto.livestock_id)
        livestock.record_nutrition_metrics(NutritionMetrics(
            feed_intake_kg=input_dto.feed_intake_kg,
            water_intake_l=input_dto.water_intake_l,
            feeder_station_id=input_dto.feeder_station_id,
        ))
        self.repo.save(livestock)
        return {"livestock_id": livestock.id}
