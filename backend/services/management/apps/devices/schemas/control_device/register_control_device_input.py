from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class RegisterControlDeviceInput:
    serial: str
    farm_id: str
    barn_id: str
    zone_id: str
    created_by: str
    display_name: str | None = None
    metadata: Dict[str, Any] | None = None
    capabilities: Dict[str, Any] | None = None
    kind: str | None = None

    def to_dict(self) -> dict:
        data = {
            "serial": self.serial,
            "farm_id": self.farm_id,
            "barn_id": self.barn_id,
            "zone_id": self.zone_id,
            "created_by": self.created_by,
            "display_name": self.display_name,
            "metadata": self.metadata,
            "capabilities": self.capabilities,
            "kind": self.kind,
        }

        return {key: value for key, value in data.items() if value is not None}
