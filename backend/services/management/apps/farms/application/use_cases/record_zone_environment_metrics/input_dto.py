# farm/application/use_cases/record_zone_environment_metrics/input_dto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class RecordZoneEnvironmentInputDTO:
    farm_id: str
    barn_id: str
    zone_id: str
    temperature_c: float
    humidity: float
    ammonia_ppm: float
    co2_ppm: Optional[float]
    airflow_mps: Optional[float]
