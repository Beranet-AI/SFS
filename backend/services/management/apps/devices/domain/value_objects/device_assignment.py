from dataclasses import dataclass
from backend.shared.ids.device_id import DeviceId
from backend.shared.ids.livestock_id import LivestockId
from datetime import datetime

@dataclass(frozen=True)
class DeviceAssignment:
    device_id: DeviceId
    livestock_id: LivestockId
    assigned_at: datetime
