from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ReceiveRawTelemetryOutput:
    payload: Dict[str, Any]
    source: str
