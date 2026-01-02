# application/use_cases/register_schema/use_case.py

from .input_dto import RegisterSchemaInputDTO
from .output_dto import RegisterSchemaOutputDTO
from ....infrastructure.models.schema_model import TelemetrySchemaModel


class RegisterTelemetrySchemaUseCase:
    """
    Registers new schema (inactive)
    """

    def execute(self, input_dto: RegisterSchemaInputDTO) -> RegisterSchemaOutputDTO:
        version = TelemetrySchemaModel.next_version(input_dto.device_type)

        schema = TelemetrySchemaModel.objects.create(
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
