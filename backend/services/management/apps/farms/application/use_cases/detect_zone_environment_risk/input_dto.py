from ....domain.value_objects.environmental_metrics import EnvironmentalMetrics
from dataclasses import dataclass

@dataclass
class DetectZoneEnvironmentRiskInputDTO:
    farm_id: str
    barn_id: str
    zone_id: str
    metrics: EnvironmentalMetrics
