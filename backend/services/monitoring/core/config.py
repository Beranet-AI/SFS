import os

SERVICE_NAME = "monitoring"

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
TELEMETRY_SERVICE_BASE = os.getenv(
    "TELEMETRY_SERVICE_BASE",
    "http://data_ingestion:8001",
)
