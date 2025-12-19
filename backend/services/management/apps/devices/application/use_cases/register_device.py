from apps.devices.domain.entities.device import Device
from apps.devices.domain.enums.device_status import DeviceStatus
from shared.ids.device_id import DeviceId

class RegisterDeviceUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, device_id: DeviceId, serial: str, device_type):
        device = Device(
            id=device_id,
            serial=serial,
            device_type=device_type,
            status=DeviceStatus.ACTIVE,
        )
        self.repo.save(device)
        return device
