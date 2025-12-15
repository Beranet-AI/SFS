from dataclasses import dataclass
from typing import Optional, List

from core.value_objects.identifiers import UUID
from core.value_objects.timestamps import ISODateString
from core.enums.device import DeviceKind, SensorMetric


@dataclass(frozen=True)
class DeviceEntity:
    id: UUID

    farm_id: UUID
    barn_id: Optional[UUID]
    zone_id: Optional[UUID]

    name: str
    kind: DeviceKind

    ip_address: Optional[str]

    metrics: Optional[List[SensorMetric]]

    is_active: bool
    created_at: ISODateString
