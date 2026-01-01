# File: livestock/application/use_cases/generate_livestock_ai_insights/use_case.py
class GenerateLivestockAIInsightsUseCase:
    def __init__(self, repo, risk_evaluator, ai_adapter):
        self.repo = repo
        self.risk = risk_evaluator
        self.ai = ai_adapter

    def execute(self, input_dto):
        livestock = self.repo.get_by_id(input_dto.livestock_id)
        if livestock.health is None:
            return {"livestock_id": livestock.id, "risk_score": None, "health_score": None, "ai": None,
                    "appetite_change": None, "abnormal_milk_drop": None, "treatment_response": None}

        risk_score = self.risk.score(livestock.health)
        health_score = self.risk.health_score(risk_score)
        ai_result = self.ai.analyze_health(livestock.health)

        # نمونهٔ خروجی‌های تحلیلی (در نسخه صنعتی از تاریخچه و آمار استفاده می‌شود)
        appetite_change = "UNKNOWN"
        abnormal_milk_drop = None
        treatment_response = "UNKNOWN"

        return {
            "livestock_id": livestock.id,
            "risk_score": risk_score,
            "health_score": health_score,
            "ai": ai_result,
            "appetite_change": appetite_change,
            "abnormal_milk_drop": abnormal_milk_drop,
            "treatment_response": treatment_response,
        }
