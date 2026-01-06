from datetime import datetime
from typing import Any, Dict, Literal

from pydantic import BaseModel, Field


class ExecuteCommandRequest(BaseModel):
    command_id: str
    command_type: Literal["DISCOVER", "ON_OFF", "REBOOT"]
    edge_id: str
    issued_at: datetime
    payload: Dict[str, Any] = Field(default_factory=dict)
