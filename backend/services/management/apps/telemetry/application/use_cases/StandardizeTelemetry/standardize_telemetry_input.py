from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class StandardizeTelemetryInput:
    payload: Dict[str, Any]
    source: str
