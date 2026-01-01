# farm/api/views.py
from .base import BaseAPIView
from .serializers.environment_metrics_serializer import EnvironmentMetricsSerializer
from ..application.use_cases.record_zone_environment_metrics.input_dto import RecordZoneEnvironmentInputDTO
from ..application.use_cases.record_zone_environment_metrics.use_case import RecordZoneEnvironmentMetricsUseCase

class RecordZoneEnvironmentView(BaseAPIView):
    def post(self, request, farm_id, barn_id, zone_id):
        s = EnvironmentMetricsSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        dto = RecordZoneEnvironmentInputDTO(
            farm_id=farm_id,
            barn_id=barn_id,
            zone_id=zone_id,
            **s.validated_data
        )
        result = RecordZoneEnvironmentMetricsUseCase(
            request.app_context.farm_repo
        ).execute(dto)

        return self.ok(result)
