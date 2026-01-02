from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ReceiveRawTelemetryInput:
    payload: Dict[str, Any]
    source: str
