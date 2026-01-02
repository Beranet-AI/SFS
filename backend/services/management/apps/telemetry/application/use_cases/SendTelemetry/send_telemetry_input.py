from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SendTelemetryInput:
    standardized: List[Dict[str, Any]]
