# File: livestock/domain/domain_services/livestock_ai_adapter.py
class LivestockAIAdapter:
    """
    اینجا قرارداد AI است؛ IO واقعی در infrastructure/client انجام می‌شود.
    """
    def analyze_health(self, metrics) -> dict:
        # Stub
        risk = "HIGH" if metrics.temperature_c >= 39 else "NORMAL"
        return {"risk_level": risk, "explanation": "stub"}
