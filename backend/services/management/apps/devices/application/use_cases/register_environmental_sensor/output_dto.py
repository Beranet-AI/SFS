from dataclasses import dataclass


@dataclass
class RegisterEnvironmentalSensorOutputDTO:
    device_id: str
    serial: str
    schema_id: str
    schema_version: str
