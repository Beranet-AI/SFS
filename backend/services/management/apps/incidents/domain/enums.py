from enum import Enum


class IncidentSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class IncidentStatus(str, Enum):
    RAISED = "raised"
    ACK = "ack"
    RESOLVED = "resolved"
