from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional


class CommandStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    ACKED = "acked"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class RetryPolicy:
    max_attempts: int = 3
    backoff_sec: int = 5


@dataclass
class Command:
    id: str
    device_id: str
    type: str
    payload: Dict
    status: CommandStatus
    attempts: int = 0
    retry_policy: Optional[RetryPolicy] = None
