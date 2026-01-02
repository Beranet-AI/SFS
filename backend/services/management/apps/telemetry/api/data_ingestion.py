from rest_framework import status

from apps.telemetry.api.base import Base
from apps.telemetry.api.serializers import (
    DataIngestionValidationRequestSerializer,
    DataIngestionValidationResponseSerializer,
)
from apps.telemetry.application.use_cases.ResponseValidation.use_case import (
    ResponseValidationUseCase,
)
from apps.telemetry.application.use_cases.ResponseValidation.response_validation_input import (
    ResponseValidationInput,
)


class DataIngestionValidationView(Base):
    request_serializer_class = DataIngestionValidationRequestSerializer
    response_serializer_class = DataIngestionValidationResponseSerializer

    def post(self, request):
        data = self.validate_request(request)

        use_case = ResponseValidationUseCase()
        result = use_case.execute(ResponseValidationInput(payload=data["payload"]))

        return self.success(
            {
                "valid": result.valid,
                "details": result.details or {},
            },
            http_status=status.HTTP_200_OK,
        )
