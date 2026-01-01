# File: farm/domain/entities/zone.py
from typing import Optional
from ..value_objects.environmental_metrics import EnvironmentalMetrics

class Zone:
    def __init__(self, zone_id: str, name: str):
        self.id = zone_id
        self.name = name
        self.environment: Optional[EnvironmentalMetrics] = None

    def update_environment(self, metrics: EnvironmentalMetrics):
        self.environment = metrics
