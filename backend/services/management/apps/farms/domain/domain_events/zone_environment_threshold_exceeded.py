class ZoneEnvironmentThresholdExceeded:
    def __init__(self, farm_id: str, zone_id: str, metrics):
        self.farm_id = farm_id
        self.zone_id = zone_id
        self.metrics = metrics
