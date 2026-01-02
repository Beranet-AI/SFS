from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class StandardizeTelemetryOutput:
    standardized: List[Dict[str, Any]]
