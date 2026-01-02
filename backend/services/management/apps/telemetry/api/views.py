# backend/services/management/apps/telemetry/api/views.py

from rest_framework import status

from apps.telemetry.api.base import Base
from .serializers import (
    ApproveTelemetrySchemaRequestSerializer,
    ApproveTelemetrySchemaResponseSerializer,
)

from apps.telemetry.application.use_cases.ApproveTelemetrySchema.use_case import (
    ApproveTelemetrySchemaUseCase,
)
from apps.telemetry.application.use_cases.ApproveTelemetrySchema.approve_telemetry_schema_input import (
    ApproveTelemetrySchemaInput,
)


class ApproveTelemetrySchemaView(Base):
    request_serializer_class = ApproveTelemetrySchemaRequestSerializer
    response_serializer_class = ApproveTelemetrySchemaResponseSerializer

    def post(self, request, schema_id):
        self.validate_request(request)

        dto = ApproveTelemetrySchemaInput(
            schema_id=str(schema_id),
            approved_by=str(self.user_id or "system"),
        )

        use_case = ApproveTelemetrySchemaUseCase()
        result = use_case.execute(dto)

        return self.success(
            {
                "schema_id": result.schema_id,
                "status": result.status,
                "activated_version": result.activated_version,
            },
            http_status=status.HTTP_200_OK,
        )
