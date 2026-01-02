from django.db import transaction

from apps.devices.application.services.device_service import DeviceService
from apps.devices.application.use_cases.register_environmental_sensor.input_dto import (
    RegisterEnvironmentalSensorInputDTO,
)
from apps.devices.application.use_cases.register_environmental_sensor.output_dto import (
    RegisterEnvironmentalSensorOutputDTO,
)
from apps.devices.models import DeviceStatus
from apps.telemetry.application.use_cases.RegisterTelemetrySchema.register_telemetry_schema_input import (
    RegisterTelemetrySchemaInput,
)
from apps.telemetry.application.use_cases.RegisterTelemetrySchema.use_case import (
    RegisterTelemetrySchemaUseCase,
)


class RegisterEnvironmentalSensorUseCase:
    def __init__(
        self,
        *,
        device_service: DeviceService | None = None,
        register_schema_uc: RegisterTelemetrySchemaUseCase | None = None,
    ) -> None:
        self._device_service = device_service or DeviceService()
        self._register_schema_uc = (
            register_schema_uc or RegisterTelemetrySchemaUseCase()
        )

    @transaction.atomic
    def execute(
        self, input_dto: RegisterEnvironmentalSensorInputDTO
    ) -> RegisterEnvironmentalSensorOutputDTO:
        device = self._device_service.register_or_update(
            serial=input_dto.serial,
            kind=input_dto.kind or "sensor",
            display_name=input_dto.display_name,
            metadata=input_dto.metadata,
            capabilities=input_dto.capabilities,
            farm_id=input_dto.farm_id,
            barn_id=input_dto.barn_id,
            zone_id=input_dto.zone_id,
            status=DeviceStatus.ACTIVE,
        )

        schema_output = self._register_schema_uc.execute(
            RegisterTelemetrySchemaInput(
                serial=input_dto.serial,
                device_type=input_dto.device_type,
                json_schema=input_dto.json_schema,
                raw_example=input_dto.raw_example,
                created_by=input_dto.created_by,
                farm_id=input_dto.farm_id,
                barn_id=input_dto.barn_id,
                zone_id=input_dto.zone_id,
                display_name=input_dto.display_name,
                metadata=input_dto.metadata,
                capabilities=input_dto.capabilities,
                kind=input_dto.kind,
            )
        )

        return RegisterEnvironmentalSensorOutputDTO(
            device_id=str(device.id),
            serial=device.serial,
            schema_id=schema_output.schema_id,
            schema_version=schema_output.version,
        )
