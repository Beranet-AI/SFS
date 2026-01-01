# File: livestock/domain/specifications/requires_attention.py
class RequiresAttention:
    def is_satisfied_by(self, health_metrics) -> bool:
        return health_metrics.temperature_c >= 39.0
