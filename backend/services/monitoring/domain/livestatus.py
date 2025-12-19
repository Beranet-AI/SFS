from dataclasses import dataclass
from datetime import datetime
from shared.ids.device_id import DeviceId
from shared.ids.livestock_id import LivestockId

@dataclass
class LiveStatus:
    """
    Operational snapshot (event == livestatus).
    """
    device_id: DeviceId
    livestock_id: LivestockId
    metric: str
    value: float
    recorded_at: datetime
