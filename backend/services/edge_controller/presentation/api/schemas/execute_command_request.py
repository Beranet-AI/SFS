from datetime import datetime
from typing import Any, Dict, Literal

from pydantic import BaseModel, Field, validator


class ExecuteCommandRequest(BaseModel):
    command_id: str
    command_type: Literal["DISCOVER", "ON_OFF", "REBOOT"]
    edge_id: str
    issued_at: datetime
    payload: Dict[str, Any] = Field(default_factory=dict)

    @validator("command_type", pre=True)
    def map_command_type(cls, value: str) -> str:
        if value in {"get_connected_devices", "GET_CONNECTED_DEVICES"}:
            return "DISCOVER"
        return value
