# File: livestock/domain/domain_services/livestock_health_analyzer.py
class LivestockHealthAnalyzer:
    def is_fever(self, temperature_c: float) -> bool:
        return temperature_c >= 39.0

    def is_severe(self, temperature_c: float) -> bool:
        return temperature_c >= 41.0
