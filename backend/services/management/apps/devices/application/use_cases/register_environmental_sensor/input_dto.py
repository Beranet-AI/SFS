from dataclasses import dataclass

from apps.devices.schemas.environmental_sensor.register_environmental_sensor_input import (
    RegisterEnvironmentalSensorInput,
)


@dataclass
class RegisterEnvironmentalSensorInputDTO(RegisterEnvironmentalSensorInput):
    serial: str
    device_type: str
    json_schema: dict
    raw_example: dict
    farm_id: str
    barn_id: str
    zone_id: str
    created_by: str
    approved_by: str
