from jsonschema import validate, ValidationError

from ...services.schema_service import SchemaService
from .response_validation_input import ResponseValidationInput
from .response_validation_output import ResponseValidationOutput


class ResponseValidationUseCase:
    def __init__(self, schema_service: SchemaService | None = None) -> None:
        self._schema_service = schema_service or SchemaService()

    def execute(
        self, input_dto: ResponseValidationInput
    ) -> ResponseValidationOutput:
        device_type = input_dto.payload.get("device_type")
        schema = self._schema_service.get_active_schema(device_type)
        if not schema:
            return ResponseValidationOutput(
                valid=False,
                details={"error": "No active schema for device type"},
            )

        try:
            validate(instance=input_dto.payload, schema=schema.json_schema)
        except ValidationError as exc:
            return ResponseValidationOutput(
                valid=False, details={"error": str(exc)}
            )

        return ResponseValidationOutput(valid=True, details=None)
