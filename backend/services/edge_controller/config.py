import os

EDGE_ID = os.getenv("EDGE_ID", "edge-001")

MQTT_BROKER = os.getenv("MQTT_BROKER_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))

MANAGEMENT_ENDPOINT = os.getenv("MANAGEMENT_ENDPOINT", "http")
MANAGEMENT_COMMANDS_BASE_URL = os.getenv(
    "MANAGEMENT_COMMANDS_BASE_URL",
    "http://management:8000/commands",
)
