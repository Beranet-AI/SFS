from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class ErrorDTO:
    error_code: str
    error_type: str
    message: str
    occurred_at: datetime
    command_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
