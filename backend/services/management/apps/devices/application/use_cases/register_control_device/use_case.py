from django.db import transaction

from apps.devices.application.services.device_service import DeviceService
from apps.devices.application.use_cases.register_control_device.input_dto import (
    RegisterControlDeviceInputDTO,
)
from apps.devices.application.use_cases.register_control_device.output_dto import (
    RegisterControlDeviceOutputDTO,
)
from apps.devices.models import DeviceStatus


class RegisterControlDeviceUseCase:
    def __init__(self, service: DeviceService | None = None) -> None:
        self._service = service or DeviceService()

    @transaction.atomic
    def execute(
        self, input_dto: RegisterControlDeviceInputDTO
    ) -> RegisterControlDeviceOutputDTO:
        device = self._service.register_or_update(
            serial=input_dto.serial,
            kind=input_dto.kind or "actuator",
            display_name=input_dto.display_name,
            metadata=input_dto.metadata,
            capabilities=input_dto.capabilities,
            farm_id=input_dto.farm_id,
            barn_id=input_dto.barn_id,
            zone_id=input_dto.zone_id,
            status=DeviceStatus.ACTIVE,
        )

        return RegisterControlDeviceOutputDTO(
            device_id=str(device.id),
            serial=device.serial,
        )
