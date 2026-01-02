# application/use_cases/validate_telemetry/use_case.py

from jsonschema import validate, ValidationError

from .output_dto import ValidateTelemetryOutputDTO
from ...services.schema_service import SchemaService
from ....infrastructure.mappers.telemetry_mapper import TelemetryMapper


class ValidateTelemetryUseCase:
    """
    Executes JSON Schema validation
    """

    def __init__(self):
        self._schema_service = SchemaService()
        self._mapper = TelemetryMapper()

    def execute(self, raw_payload: dict, device_id: str) -> ValidateTelemetryOutputDTO:
        # device_type resolution is simplified for now
        device_type = raw_payload.get("device_type")

        schema = self._schema_service.get_active_schema(device_type)
        if not schema:
            raise ValueError("No active schema for device type")

        try:
            validate(instance=raw_payload, schema=schema.json_schema)
        except ValidationError as exc:
            raise ValueError(f"Telemetry schema validation failed: {exc}")

        domain_obj = self._mapper.raw_to_domain(raw_payload)

        return ValidateTelemetryOutputDTO(
            domain_telemetry=domain_obj,
            schema_version=schema.version,
        )
