from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ValidateRawTelemetryInput:
    payload: Dict[str, Any]
