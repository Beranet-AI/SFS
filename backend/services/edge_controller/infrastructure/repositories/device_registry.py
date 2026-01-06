from ...domain.repositories.device_registry import DeviceRegistry
from ...domain.value_objects.device_id import DeviceId


class InMemoryDeviceRegistry(DeviceRegistry):
    """
    Runtime registry of approved / active devices.
    """

    def __init__(self) -> None:
        self._approved_devices: set[str] = set()

    def approve(self, device_id: DeviceId) -> None:
        self._approved_devices.add(device_id.value)

    def remove(self, device_id: DeviceId) -> None:
        self._approved_devices.discard(device_id.value)

    def is_registered(self, device_id: DeviceId) -> bool:
        if not self._approved_devices:
            return bool(device_id.value)

        return device_id.value in self._approved_devices
