from datetime import datetime
from pydantic import BaseModel

class HeartbeatSchema(BaseModel):
    node_id: str
    name: str
    ip: str

class DiscoverySchema(BaseModel):
    node_id: str
    discovered_devices: list[dict]
    reported_at: datetime | None = None

class ForwardTelemetrySchema(BaseModel):
    device_id: str
    livestock_id: str
    metric: str
    value: float
    recorded_at: datetime | None = None
