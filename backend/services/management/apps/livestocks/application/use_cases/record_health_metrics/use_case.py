# File: livestock/application/use_cases/record_health_metrics/use_case.py
from ....domain.value_objects.health_metrics import HealthMetrics

class RecordHealthMetricsUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, input_dto):
        livestock = self.repo.get_by_id(input_dto.livestock_id)
        metrics = HealthMetrics(
            temperature_c=input_dto.temperature_c,
            activity=input_dto.activity,
            rumination_minutes=input_dto.rumination_minutes,
            movement_index=input_dto.movement_index,
            lying_minutes=input_dto.lying_minutes,
            standing_minutes=input_dto.standing_minutes,
            heart_rate_bpm=input_dto.heart_rate_bpm,
        )
        livestock.record_health_metrics(metrics)
        self.repo.save(livestock)
        events = [e.__class__.__name__ for e in livestock.pull_events()]
        return {"livestock_id": livestock.id, "events": events}
