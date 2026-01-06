from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field


class ReceiveTelemetryRequest(BaseModel):
    edge_id: str
    device_id: str
    device_type: str
    timestamp: datetime
    metrics: Dict[str, float]
    meta: Dict[str, Any] | None = Field(default=None)
