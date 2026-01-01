# farm/application/use_cases/record_farm_economic_metrics/input_dto.py
from dataclasses import dataclass

@dataclass
class RecordFarmEconomicInputDTO:
    farm_id: str
    feed_cost: float
    treatment_cost: float
    revenue: float
