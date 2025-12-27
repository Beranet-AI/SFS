from pydantic import BaseModel
from typing import Optional, Dict
from backend.shared.enums.command_status import CommandStatus

class CommandDTO(BaseModel):
    command_id: str
    device_id: str
    command_type: str
    payload: Dict
    status: CommandStatus
    retries: int
    max_retries: int
    issued_by: str  # manual | rule | ai
    correlation_id: Optional[str] = None
