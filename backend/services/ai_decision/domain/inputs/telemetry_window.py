from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TelemetryPoint:
    metric: str
    value: float
    recorded_at: datetime

@dataclass(frozen=True)
class TelemetryWindow:
    """
    Sliding window of telemetry for inference.
    """
    livestock_id: str
    points: list[TelemetryPoint]
