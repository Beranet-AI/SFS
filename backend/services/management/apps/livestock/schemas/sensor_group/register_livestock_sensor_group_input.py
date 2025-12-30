from dataclasses import dataclass
from typing import List


@dataclass
class RegisterLivestockSensorGroupInput:
    livestock_id: str
    rfid_device_id: str
    sensor_device_ids: List[str]

    def to_dict(self) -> dict:
        return {
            "livestock_id": self.livestock_id,
            "rfid_device_id": self.rfid_device_id,
            "sensor_device_ids": self.sensor_device_ids,
        }
