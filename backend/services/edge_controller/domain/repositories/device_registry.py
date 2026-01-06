from typing import Protocol

from ..value_objects.device_id import DeviceId


class DeviceRegistry(Protocol):
    def is_registered(self, device_id: DeviceId) -> bool:
        ...
