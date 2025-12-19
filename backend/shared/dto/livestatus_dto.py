from datetime import datetime
from shared.ids.device_id import DeviceId
from shared.ids.livestock_id import LivestockId

class LiveStatusDTO:
    """
    Operational live status (event/livestatus).
    Read-only snapshot.
    """

    def __init__(
        self,
        device_id: DeviceId,
        livestock_id: LivestockId,
        metric: str,
        value: float,
        recorded_at: datetime
    ):
        self.device_id = device_id
        self.livestock_id = livestock_id
        self.metric = metric
        self.value = value
        self.recorded_at = recorded_at
