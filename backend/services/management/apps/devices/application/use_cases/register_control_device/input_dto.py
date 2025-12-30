from dataclasses import dataclass

from apps.devices.schemas.control_device.register_control_device_input import (
    RegisterControlDeviceInput,
)


@dataclass
class RegisterControlDeviceInputDTO(RegisterControlDeviceInput):
    serial: str
    farm_id: str
    barn_id: str
    zone_id: str
    created_by: str
