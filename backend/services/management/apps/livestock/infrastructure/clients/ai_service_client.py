# File: livestock/infrastructure/clients/ai_service_client.py
class LivestockAIServiceClient:
    def infer(self, payload: dict) -> dict:
        return {"risk_level": "NORMAL", "reason": "stub"}
