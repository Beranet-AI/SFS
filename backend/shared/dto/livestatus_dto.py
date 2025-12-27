from __future__ import annotations

from pydantic import BaseModel, Field


class LiveStatusEventDTO(BaseModel):
    device_id: str = Field(..., min_length=1)
    ts: str  # ISO time from producer (edge/data_ingestion)
    metric: str = Field(..., min_length=1)
    value: float
    unit: str | None = None
    meta: dict | None = None
