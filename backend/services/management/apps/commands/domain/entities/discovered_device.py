from dataclasses import dataclass

from apps.commands.domain.enums.discovered_device_status import (
    DiscoveredDeviceStatus,
)


@dataclass(frozen=True)
class DiscoveredDevice:
    id: str
    session_id: str
    device_id: str
    device_type: str
    ip_address: str | None
    status: DiscoveredDeviceStatus
    capabilities: dict
    raw_payload: dict
    registered_device_id: str | None
