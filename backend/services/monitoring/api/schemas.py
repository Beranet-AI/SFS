from datetime import datetime
from pydantic import BaseModel

class LiveStatusSchema(BaseModel):
    device_id: str
    livestock_id: str
    metric: str
    value: float
    recorded_at: datetime
