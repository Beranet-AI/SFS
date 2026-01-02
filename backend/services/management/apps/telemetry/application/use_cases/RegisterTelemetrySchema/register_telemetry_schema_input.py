from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class RegisterTelemetrySchemaInput:
    serial: str
    device_type: str
    json_schema: Dict[str, Any]
    raw_example: Dict[str, Any]
    created_by: str
    farm_id: str | None = None
    barn_id: str | None = None
    zone_id: str | None = None
    livestock_id: str | None = None
    display_name: str | None = None
    metadata: Dict[str, Any] | None = None
    capabilities: Dict[str, Any] | None = None
    kind: str | None = None
