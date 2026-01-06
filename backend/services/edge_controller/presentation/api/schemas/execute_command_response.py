from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ExecuteCommandResponse(BaseModel):
    command_id: str
    command_type: str
    status: str
    executed_at: datetime
    devices: Optional[List[Dict[str, Any]]] = None
    device_id: Optional[str] = None
    execution_state: Optional[str] = None
    reboot_state: Optional[str] = None
