from __future__ import annotations

from pydantic import BaseModel, Field


class HeartbeatInDTO(BaseModel):
    device_id: str = Field(..., min_length=1)
    # Optional: you can extend with firmware, ip, etc.
    meta: dict | None = None


class HealthSnapshotDTO(BaseModel):
    device_id: str
    health: str
    last_seen_at: str | None
    server_time: str
