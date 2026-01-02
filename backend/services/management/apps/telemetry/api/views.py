# backend/services/management/apps/telemetry/api/views.py

from rest_framework import status

from apps.telemetry.api.base import Base
from .serializers import (
    ApproveTelemetrySchemaRequestSerializer,
    ApproveTelemetrySchemaResponseSerializer,
)

from apps.telemetry.application.use_cases.approve_schema.use_case import (
    ApproveTelemetrySchemaUseCase,
)
from apps.telemetry.application.use_cases.approve_schema.input_dto import (
    ApproveTelemetrySchemaInputDTO,
)


class ApproveTelemetrySchemaView(Base):
    request_serializer_class = ApproveTelemetrySchemaRequestSerializer
    response_serializer_class = ApproveTelemetrySchemaResponseSerializer

    def post(self, request, schema_id):
        data = self.validate_request(request)

        dto = ApproveTelemetrySchemaInputDTO(
            schema_id=schema_id,
            approved=data["approved"],
            approved_by=self.user_id,
        )

        use_case = ApproveTelemetrySchemaUseCase()
        result = use_case.execute(dto)

        return self.success(
            {
                "schema_id": result.schema_id,
                "status": result.status,
            },
            http_status=status.HTTP_200_OK,
        )
