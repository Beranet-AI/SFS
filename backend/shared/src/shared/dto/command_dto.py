from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime


@dataclass(frozen=True)
class CommandDTO:
    """
    Command sent from Management (manual) or AI (automatic) to Edge Controller.
    """
    command_id: str
    target_device_serial: str
    command_type: str   # e.g. FAN_SET_SPEED, VALVE_OPEN, OZONE_INJECT, REBOOT
    params: Dict[str, Any] = field(default_factory=dict)

    issued_by: str = "system"  # admin | ai | system
    ts: datetime = field(default_factory=datetime.utcnow)

    # optional: ack tracking
    correlation_id: Optional[str] = None
