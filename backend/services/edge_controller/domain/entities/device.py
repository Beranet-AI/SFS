from dataclasses import dataclass

from ..value_objects.device_id import DeviceId


@dataclass(frozen=True)
class Device:
    device_id: DeviceId
    device_type: str
