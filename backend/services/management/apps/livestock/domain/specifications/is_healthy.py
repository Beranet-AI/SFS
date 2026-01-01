# File: livestock/domain/specifications/is_healthy.py
class IsHealthy:
    def is_satisfied_by(self, health_metrics) -> bool:
        return health_metrics.temperature_c < 39.0
