from django.db import transaction

from apps.devices.application.services.device_service import DeviceService

from .register_telemetry_schema_input import RegisterTelemetrySchemaInput
from .register_telemetry_schema_output import RegisterTelemetrySchemaOutput
from ....infrastructure.models.schema_model import TelemetrySchemaModel


class RegisterTelemetrySchemaUseCase:
    def __init__(self, device_service: DeviceService | None = None) -> None:
        self._device_service = device_service or DeviceService()

    @transaction.atomic
    def execute(
        self, input_dto: RegisterTelemetrySchemaInput
    ) -> RegisterTelemetrySchemaOutput:
        device = self._device_service.register_or_update(
            serial=input_dto.serial,
            kind=input_dto.kind or "sensor",
            display_name=input_dto.display_name,
            metadata=input_dto.metadata,
            capabilities=input_dto.capabilities,
            farm_id=input_dto.farm_id,
            barn_id=input_dto.barn_id,
            zone_id=input_dto.zone_id,
        )

        if input_dto.livestock_id is not None:
            self._device_service.assign(
                device=device, livestock_id=input_dto.livestock_id
            )

        version = TelemetrySchemaModel.next_version(input_dto.device_type)
        schema = TelemetrySchemaModel.objects.create(
            device_type=input_dto.device_type,
            json_schema=input_dto.json_schema,
            raw_example=input_dto.raw_example,
            version=version,
            is_active=False,
            created_by=input_dto.created_by,
        )

        return RegisterTelemetrySchemaOutput(
            device_id=str(device.id),
            schema_id=str(schema.id),
            version=version,
        )
