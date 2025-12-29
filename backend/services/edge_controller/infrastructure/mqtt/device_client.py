import json
from ...core.logging import get_logger

logger = get_logger("DeviceMqttClient")

class DeviceClient:
    def publish(self, topic: str, payload: dict):
        """
        Send command to physical device.
        """
        logger.info(f"[DEVICE MQTT] Publish to {topic}: {payload}")

        # placeholder for real mqtt publish
        # mqtt_client.publish(topic, json.dumps(payload))

    def send_reboot(self, device_id: str) -> bool:
        topic = self._topics.reboot(device_id)
        payload = {"action": "REBOOT"}
        return self._publish(topic, payload)

