# File: livestock/api/views.py
from .base import BaseAPIView
from .serializers.livestock_identity_serializer import LivestockIdentitySerializer
from .serializers.health_metrics_serializer import HealthMetricsSerializer
from .serializers.nutrition_metrics_serializer import NutritionMetricsSerializer
from .serializers.milk_production_serializer import MilkProductionSerializer
from .serializers.reproduction_serializer import ReproductionSerializer
from .serializers.disease_serializer import TreatmentSerializer

from ..application.use_cases.register_livestock.input_dto import RegisterLivestockInputDTO
from ..application.use_cases.register_livestock.use_case import RegisterLivestockUseCase

from ..application.use_cases.record_health_metrics.input_dto import RecordHealthMetricsInputDTO
from ..application.use_cases.record_health_metrics.use_case import RecordHealthMetricsUseCase

from ..application.use_cases.record_nutrition_metrics.input_dto import RecordNutritionMetricsInputDTO
from ..application.use_cases.record_nutrition_metrics.use_case import RecordNutritionMetricsUseCase

from ..application.use_cases.record_milk_production.input_dto import RecordMilkProductionInputDTO
from ..application.use_cases.record_milk_production.use_case import RecordMilkProductionUseCase

from ..application.use_cases.evaluate_reproduction_status.input_dto import EvaluateReproductionStatusInputDTO
from ..application.use_cases.evaluate_reproduction_status.use_case import EvaluateReproductionStatusUseCase

from ..application.use_cases.record_treatment.input_dto import RecordTreatmentInputDTO
from ..application.use_cases.record_treatment.use_case import RecordTreatmentUseCase

from ..application.use_cases.generate_livestock_ai_insights.input_dto import GenerateLivestockAIInsightsInputDTO
from ..application.use_cases.generate_livestock_ai_insights.use_case import GenerateLivestockAIInsightsUseCase

class RegisterLivestockView(BaseAPIView):
    def post(self, request):
        s = LivestockIdentitySerializer(data=request.data)
        s.is_valid(raise_exception=True)
        dto = RegisterLivestockInputDTO(**s.validated_data)
        result = RegisterLivestockUseCase(request.app_context.livestock_repo).execute(dto)
        return self.ok(result, status=201)

class RecordHealthMetricsView(BaseAPIView):
    def post(self, request, livestock_id: str):
        s = HealthMetricsSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        dto = RecordHealthMetricsInputDTO(livestock_id=livestock_id, **s.validated_data)
        result = RecordHealthMetricsUseCase(request.app_context.livestock_repo).execute(dto)
        return self.ok(result)

class RecordNutritionMetricsView(BaseAPIView):
    def post(self, request, livestock_id: str):
        s = NutritionMetricsSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        dto = RecordNutritionMetricsInputDTO(livestock_id=livestock_id, **s.validated_data)
        result = RecordNutritionMetricsUseCase(request.app_context.livestock_repo).execute(dto)
        return self.ok(result)

class RecordMilkProductionView(BaseAPIView):
    def post(self, request, livestock_id: str):
        s = MilkProductionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        dto = RecordMilkProductionInputDTO(livestock_id=livestock_id, **s.validated_data)
        result = RecordMilkProductionUseCase(request.app_context.livestock_repo).execute(dto)
        return self.ok(result)

class RecordReproductionView(BaseAPIView):
    def post(self, request, livestock_id: str):
        s = ReproductionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        dto = EvaluateReproductionStatusInputDTO(livestock_id=livestock_id, **s.validated_data)
        result = EvaluateReproductionStatusUseCase(request.app_context.livestock_repo).execute(dto)
        return self.ok(result)

class RecordTreatmentView(BaseAPIView):
    def post(self, request, livestock_id: str):
        s = TreatmentSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        dto = RecordTreatmentInputDTO(livestock_id=livestock_id, **s.validated_data)
        result = RecordTreatmentUseCase(request.app_context.livestock_repo).execute(dto)
        return self.ok(result)

class LivestockAIInsightsView(BaseAPIView):
    def get(self, request, livestock_id: str):
        dto = GenerateLivestockAIInsightsInputDTO(livestock_id=livestock_id)
        result = GenerateLivestockAIInsightsUseCase(
            request.app_context.livestock_repo,
            request.app_context.livestock_risk_evaluator,
            request.app_context.livestock_ai_adapter,
        ).execute(dto)
        return self.ok(result)
