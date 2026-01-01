# application/use_cases/register_schema/use_case.py

from .input_dto import RegisterSchemaInputDTO
from .output_dto import RegisterSchemaOutputDTO
from ....infrastructure.models.telemetry_schema import TelemetrySchema


class RegisterTelemetrySchemaUseCase:
    """
    Registers new schema (inactive)
    """

    def execute(self, input_dto: RegisterSchemaInputDTO) -> RegisterSchemaOutputDTO:
        version = TelemetrySchema.next_version(input_dto.device_type)

        schema = TelemetrySchema.objects.create(
            device_type=input_dto.device_type,
            json_schema=input_dto.json_schema,
            raw_example=input_dto.raw_example,
            version=version,
            is_active=False,
            created_by=input_dto.created_by,
        )

        return RegisterSchemaOutputDTO(
            schema_id=str(schema.id),
            version=version,
        )
