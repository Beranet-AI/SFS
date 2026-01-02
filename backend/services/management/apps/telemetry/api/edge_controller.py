from rest_framework import status

from apps.telemetry.api.base import Base
from apps.telemetry.api.serializers import (
    EdgeControllerTelemetryRequestSerializer,
    EdgeControllerTelemetryResponseSerializer,
)
from apps.telemetry.application.services.telemetry_service import TelemetryService


class EdgeControllerTelemetryView(Base):
    request_serializer_class = EdgeControllerTelemetryRequestSerializer
    response_serializer_class = EdgeControllerTelemetryResponseSerializer

    def post(self, request):
        data = self.validate_request(request)

        service = TelemetryService()
        result = service.receive_raw(
            payload=data,
            source="EDGE_CONTROLLER",
        )

        return self.success(result, http_status=status.HTTP_201_CREATED)
