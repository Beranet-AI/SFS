import logging
import paho.mqtt.client as mqtt

from .device_topics import DISCOVER_COMMAND

logger = logging.getLogger("mqtt")


class MQTTClient:
    def __init__(self, broker_host: str, broker_port: int, client_id: str):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client_id = client_id

        self._client = mqtt.Client(client_id=self.client_id)
        self._connected = False

        # callbacks
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

    # -------------------------------------------------
    # lifecycle
    # -------------------------------------------------

    def connect(self):
        logger.info(
            "Connecting to MQTT broker %s:%s",
            self.broker_host,
            self.broker_port,
        )
        self._client.connect(self.broker_host, self.broker_port, keepalive=60)
        self._client.loop_start()

    def disconnect(self):
        if not self._connected:
            return

        logger.info("Disconnecting from MQTT broker")
        self._client.loop_stop()
        self._client.disconnect()

    # -------------------------------------------------
    # callbacks
    # -------------------------------------------------

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self._connected = True
            logger.info("MQTT connected successfully")
        else:
            logger.error("MQTT connection failed with code %s", rc)

    def _on_disconnect(self, client, userdata, rc):
        self._connected = False
        logger.warning("MQTT disconnected with code %s", rc)

    def _on_message(self, client, userdata, msg):
        logger.info(
            "MQTT message received: topic=%s payload=%s",
            msg.topic,
            msg.payload.decode(errors="ignore"),
        )

    # -------------------------------------------------
    # messaging
    # -------------------------------------------------

    def subscribe_default_topics(self):
        """
        Subscribe to base topics required by Edge Controller.
        """
        logger.info("Subscribing to default MQTT topics")
        self._client.subscribe(DISCOVER_COMMAND)

    def publish(self, topic: str, payload: str):
        if not self._connected:
            raise RuntimeError("MQTT client is not connected")

        logger.info("Publishing MQTT message: topic=%s", topic)
        self._client.publish(topic, payload)
