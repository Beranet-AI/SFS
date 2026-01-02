from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ReceiveTelemetryInput:
    payload: Dict[str, Any]
