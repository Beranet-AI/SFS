from dataclasses import dataclass


@dataclass
class RegisterControlDeviceOutputDTO:
    device_id: str
    serial: str
