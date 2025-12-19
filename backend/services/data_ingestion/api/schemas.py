from datetime import datetime
from pydantic import BaseModel

class TelemetryIngestSchema(BaseModel):
    device_id: str
    livestock_id: str
    metric: str
    value: float
    recorded_at: datetime | None = None
