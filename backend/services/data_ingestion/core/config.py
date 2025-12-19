import os

SERVICE_NAME = "data_ingestion"

MANAGEMENT_BASE = os.getenv(
    "MANAGEMENT_BASE",
    "http://management:8000",
)

MONITORING_BASE = os.getenv(
    "MONITORING_BASE",
    "http://monitoring:8002",
)

RULES_BASE = os.getenv(
    "RULES_BASE",
    "http://management:8000/api/v1/rules",
)

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
