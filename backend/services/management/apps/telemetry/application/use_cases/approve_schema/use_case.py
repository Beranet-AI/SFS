# application/use_cases/approve_schema/use_case.py

from .input_dto import ApproveSchemaInputDTO
from .output_dto import ApproveSchemaOutputDTO
from ....infrastructure.models.schema_model import TelemetrySchemaModel
from ...services.schema_service import SchemaService


class ApproveTelemetrySchemaUseCase:
    """
    Activates schema for future telemetry
    """

    def __init__(self):
        self._schema_service = SchemaService()

    def execute(self, input_dto: ApproveSchemaInputDTO) -> ApproveSchemaOutputDTO:
        schema = TelemetrySchemaModel.objects.get(id=input_dto.schema_id)

        self._schema_service.deactivate_active_schema(schema.device_type)

        schema.is_active = True
        schema.approved_by = input_dto.approved_by
        schema.save()

        return ApproveSchemaOutputDTO(
            success=True,
            activated_version=schema.version,
        )
