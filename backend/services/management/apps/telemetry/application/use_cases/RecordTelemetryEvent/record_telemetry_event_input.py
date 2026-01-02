from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class RecordTelemetryEventInput:
    standardized: List[Dict[str, Any]]
