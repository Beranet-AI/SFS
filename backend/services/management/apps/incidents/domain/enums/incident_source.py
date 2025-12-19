from enum import Enum

class IncidentSource(str, Enum):
    RULE = "rule"
    TELEMETRY = "telemetry"
    MANUAL = "manual"
    AI = "ai"
