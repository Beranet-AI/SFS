from dataclasses import dataclass


@dataclass
class RegisterLivestockSensorGroupOutputDTO:
    group_id: str
    livestock_id: str
    rfid_device_id: str
    sensor_device_ids: list[str]
