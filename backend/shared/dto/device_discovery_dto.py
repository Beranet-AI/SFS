from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime


@dataclass(frozen=True)
class DeviceDiscoveryDTO:
    """
    Device that is seen on the edge network but not yet approved/registered
    in Management.
    """
    serial: str
    device_type: str  # e.g. temperature, humidity, fan, valve, ozone_injector
    protocol: str     # http_json | mqtt | modbus | opcua | labview
    display_name: Optional[str] = None

    # Where it is intended to be assigned after approval:
    farm_id: Optional[str] = None
    barn_id: Optional[str] = None
    zone_id: Optional[str] = None
    livestock_id: Optional[str] = None  # some sensors attach to animal

    metadata: Dict[str, Any] = field(default_factory=dict)  # vendor, fw, capabilities, etc.
    last_seen_at: Optional[datetime] = None
