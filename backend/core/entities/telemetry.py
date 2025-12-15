from dataclasses import dataclass

from core.value_objects.identifiers import UUID
from core.value_objects.timestamps import ISODateString
from core.enums.device import SensorMetric


@dataclass(frozen=True)
class TelemetryReadingEntity:
    id: UUID

    device_id: UUID
    metric: SensorMetric

    value: float
    unit: str

    timestamp: ISODateString
    received_at: ISODateString

    edge_id: UUID
