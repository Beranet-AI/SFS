from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from shared.schemas.edge_controller.forward_telemetry.telemetry_input import TelemetryInput

@dataclass
class TelemetryInputDTO(TelemetryInput):
    edge_id: str
    device_id: str
    device_type: str
    timestamp: datetime
    metrics: Dict[str, float]
    meta: Dict[str, Any] | None = None

    def to_dict(self):
        return {
            "edge_id": self.edge_id,
            "device_id": self.device_id,
            "device_type": self.device_type,
            "timestamp": self.timestamp.isoformat() + "Z",
            "metrics": self.metrics,
            "meta": self.meta or {},
        }
