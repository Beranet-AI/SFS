from enum import Enum

class IncidentStatus(str, Enum):
    OPEN = "open"
    ACKED = "acked"
    RESOLVED = "resolved"
