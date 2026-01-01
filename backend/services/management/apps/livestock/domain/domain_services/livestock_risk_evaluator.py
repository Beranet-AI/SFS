# File: livestock/domain/domain_services/livestock_risk_evaluator.py
class LivestockRiskEvaluator:
    """
    خروجی: risk_score 0..1 و health_score 0..100
    """
    def score(self, metrics) -> float:
        temp = min(max((metrics.temperature_c - 38.0) / 5.0, 0.0), 1.0)
        activity_penalty = 0.1 if metrics.activity < 0.2 else 0.0
        return min(temp + activity_penalty, 1.0)

    def health_score(self, risk_score: float) -> float:
        return max(0.0, 100.0 * (1.0 - risk_score))
