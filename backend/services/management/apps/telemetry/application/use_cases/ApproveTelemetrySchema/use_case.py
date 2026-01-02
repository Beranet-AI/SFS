from .approve_telemetry_schema_input import ApproveTelemetrySchemaInput
from .approve_telemetry_schema_output import ApproveTelemetrySchemaOutput
from ...services.schema_service import SchemaService
from ....infrastructure.models.schema_model import TelemetrySchemaModel


class ApproveTelemetrySchemaUseCase:
    def __init__(self, schema_service: SchemaService | None = None) -> None:
        self._schema_service = schema_service or SchemaService()

    def execute(
        self, input_dto: ApproveTelemetrySchemaInput
    ) -> ApproveTelemetrySchemaOutput:
        schema = TelemetrySchemaModel.objects.get(id=input_dto.schema_id)
        self._schema_service.deactivate_active_schema(schema.device_type)

        schema.approve(input_dto.approved_by)

        return ApproveTelemetrySchemaOutput(
            schema_id=str(schema.id),
            status="APPROVED",
            activated_version=schema.version,
        )
