# File: livestock/application/livestock_service.py
from .use_cases.register_livestock.use_case import RegisterLivestockUseCase
from .use_cases.record_health_metrics.use_case import RecordHealthMetricsUseCase
from .use_cases.record_nutrition_metrics.use_case import RecordNutritionMetricsUseCase
from .use_cases.record_milk_production.use_case import RecordMilkProductionUseCase
from .use_cases.evaluate_reproduction_status.use_case import EvaluateReproductionStatusUseCase
from .use_cases.record_treatment.use_case import RecordTreatmentUseCase
from .use_cases.generate_livestock_ai_insights.use_case import GenerateLivestockAIInsightsUseCase

class LivestockService:
    def __init__(self, repo, risk_evaluator, ai_adapter):
        self.repo = repo
        self.risk = risk_evaluator
        self.ai = ai_adapter

    def register_livestock(self, dto): return RegisterLivestockUseCase(self.repo).execute(dto)
    def record_health(self, dto): return RecordHealthMetricsUseCase(self.repo).execute(dto)
    def record_nutrition(self, dto): return RecordNutritionMetricsUseCase(self.repo).execute(dto)
    def record_milk(self, dto): return RecordMilkProductionUseCase(self.repo).execute(dto)
    def record_reproduction(self, dto): return EvaluateReproductionStatusUseCase(self.repo).execute(dto)
    def record_treatment(self, dto): return RecordTreatmentUseCase(self.repo).execute(dto)
    def ai_insights(self, dto): return GenerateLivestockAIInsightsUseCase(self.repo, self.risk, self.ai).execute(dto)
