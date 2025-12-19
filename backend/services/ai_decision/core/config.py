import os

SERVICE_NAME = "ai_decision"

MANAGEMENT_BASE = os.getenv(
    "MANAGEMENT_BASE",
    "http://management:8000",
)

TELEMETRY_BASE = os.getenv(
    "TELEMETRY_BASE",
    "http://management:8000/api/v1/telemetry",
)
