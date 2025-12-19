from abc import ABC, abstractmethod
from apps.devices.domain.entities.device import Device
from shared.ids.device_id import DeviceId

class DeviceRepository(ABC):

    @abstractmethod
    def get_by_id(self, device_id: DeviceId) -> Device: ...

    @abstractmethod
    def save(self, device: Device) -> None: ...
