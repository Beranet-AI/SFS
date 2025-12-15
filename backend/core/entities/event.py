from dataclasses import dataclass
from typing import Optional

from core.value_objects.identifiers import UUID
from core.value_objects.timestamps import ISODateString
from core.enums.device import SensorMetric
from core.enums.event import EventSeverity, EventStatus


@dataclass(frozen=True)
class EventEntity:
    id: UUID

    severity: EventSeverity
    status: EventStatus

    metric: Optional[SensorMetric]
    value: Optional[float]

    title: str
    message: str

    farm_id: UUID
    barn_id: Optional[UUID]
    zone_id: Optional[UUID]
    device_id: Optional[UUID]

    created_at: ISODateString
    updated_at: Optional[ISODateString]
