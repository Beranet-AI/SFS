from dataclasses import dataclass

from apps.livestock.schemas.sensor_group.register_livestock_sensor_group_input import (
    RegisterLivestockSensorGroupInput,
)


@dataclass
class RegisterLivestockSensorGroupInputDTO(RegisterLivestockSensorGroupInput):
    livestock_id: str
    rfid_device_id: str
    sensor_device_ids: list[str]
