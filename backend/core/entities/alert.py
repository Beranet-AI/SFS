from dataclasses import dataclass
from typing import Optional

from core.value_objects.identifiers import UUID
from core.value_objects.timestamps import ISODateString
from core.enums.event import EventSeverity


@dataclass(frozen=True)
class AlertEntity:
    id: UUID

    severity: EventSeverity

    title: str
    message: str

    event_id: UUID

    device_id: Optional[UUID]
    zone_id: Optional[UUID]

    timestamp: ISODateString
