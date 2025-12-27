from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class DevicePromoted:
    """
    Domain Event emitted when a discovered device
    is approved and promoted to a real Device.
    """

    discovery_id: UUID
    device_id: int
    device_serial: str
    occurred_at: datetime
