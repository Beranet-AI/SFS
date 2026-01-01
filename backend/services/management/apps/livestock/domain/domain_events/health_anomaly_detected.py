# File: livestock/domain/domain_events/health_anomaly_detected.py
class HealthAnomalyDetected:
    def __init__(self, livestock_id: str, temperature_c: float):
        self.livestock_id = livestock_id
        self.temperature_c = temperature_c
