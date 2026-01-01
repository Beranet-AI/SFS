# farm/application/use_cases/record_farm_economic_metrics/use_case.py
from ....domain.value_objects.economic_metrics import EconomicMetrics

class RecordFarmEconomicMetricsUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, dto):
        farm = self.repo.get_by_id(dto.farm_id)
        farm.set_economic_metrics(EconomicMetrics(
            feed_cost=dto.feed_cost,
            treatment_cost=dto.treatment_cost,
            revenue=dto.revenue,
        ))
        self.repo.save(farm)
        return {"farm_id": farm.id}
