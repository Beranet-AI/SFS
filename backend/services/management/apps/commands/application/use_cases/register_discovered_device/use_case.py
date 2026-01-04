from apps.commands.domain.repositories.discovered_device_repository import (
    DiscoveredDeviceRepository,
)
from apps.commands.domain.enums.discovered_device_status import (
    DiscoveredDeviceStatus,
)
from apps.devices.application.services.device_service import DeviceService
from apps.devices.models import DeviceStatus
from .input_dto import RegisterDiscoveredDeviceInputDTO


class RegisterDiscoveredDeviceUseCase:
    """
    Promote a discovered device into the managed device registry.
    """

    def __init__(
        self,
        *,
        discovered_device_repository: DiscoveredDeviceRepository,
        device_service: DeviceService | None = None,
    ) -> None:
        self._discovered_device_repository = discovered_device_repository
        self._device_service = device_service or DeviceService()

    def execute(self, dto: RegisterDiscoveredDeviceInputDTO):
        discovered = self._discovered_device_repository.get(
            discovered_device_id=dto.discovered_device_id
        )
        if discovered.status == DiscoveredDeviceStatus.REGISTERED:
            return self._device_service.get_by_serial(
                serial=discovered.device_id
            )

        metadata = dict(discovered.raw_payload or {})
        if discovered.ip_address:
            metadata["ip_address"] = discovered.ip_address

        device = self._device_service.register_or_update(
            serial=discovered.device_id,
            kind=discovered.device_type or "device",
            display_name=discovered.device_id,
            metadata=metadata,
            capabilities=discovered.capabilities,
            status=DeviceStatus.ACTIVE,
        )

        self._discovered_device_repository.mark_registered(
            discovered_device_id=discovered.id,
            registered_device_id=str(device.id),
        )

        return device
