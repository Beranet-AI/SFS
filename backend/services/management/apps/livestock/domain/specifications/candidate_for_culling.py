# File: livestock/domain/specifications/candidate_for_culling.py
class CandidateForCulling:
    def is_satisfied_by(self, health_metrics) -> bool:
        return health_metrics.temperature_c >= 41.0
