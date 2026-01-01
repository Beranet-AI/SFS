# farm/application/use_cases/record_zone_environment_metrics/use_case.py
from ....domain.value_objects.environmental_metrics import EnvironmentalMetrics

class RecordZoneEnvironmentMetricsUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, dto):
        farm = self.repo.get_by_id(dto.farm_id)
        barn = next(b for b in farm.barns if b.id == dto.barn_id)
        zone = next(z for z in barn.zones if z.id == dto.zone_id)

        zone.update_environment(EnvironmentalMetrics(
            temperature_c=dto.temperature_c,
            humidity=dto.humidity,
            ammonia_ppm=dto.ammonia_ppm,
            co2_ppm=dto.co2_ppm,
            airflow_mps=dto.airflow_mps,
        ))
        self.repo.save(farm)
        return {"zone_id": zone.id}
