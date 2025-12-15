from enum import Enum


class EventSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class EventStatus(str, Enum):
    RAISED = "raised"
    ACK = "ack"
    RESOLVED = "resolved"
