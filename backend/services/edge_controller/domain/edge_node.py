from dataclasses import dataclass
from datetime import datetime

@dataclass
class EdgeNode:
    """
    Represents an Edge gateway/controller instance.
    """
    node_id: str
    name: str
    ip: str
    last_seen: datetime
    is_online: bool = True
