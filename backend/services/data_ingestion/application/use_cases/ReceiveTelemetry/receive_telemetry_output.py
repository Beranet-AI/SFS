from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ReceiveTelemetryOutput:
    payload: Dict[str, Any]
