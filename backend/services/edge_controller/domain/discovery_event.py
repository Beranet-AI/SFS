from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class DiscoveryEvent:
    """
    Sent from edge when it discovers devices/sensors.
    """
    node_id: str
    discovered_devices: list[dict]
    reported_at: datetime
