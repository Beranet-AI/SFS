from dataclasses import dataclass


@dataclass
class RegisterDiscoveredDeviceInputDTO:
    discovered_device_id: str
