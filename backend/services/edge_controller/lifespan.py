from contextlib import asynccontextmanager

from .logging import get_logger
from . import config
from .infrastructure.mqtt.mqtt_client import MQTTClient

logger = get_logger("lifespan")


@asynccontextmanager
async def lifespan(app):
    logger.info("Edge controller starting")

    mqtt_client = MQTTClient(
        broker_host=config.MQTT_BROKER,
        broker_port=config.MQTT_PORT,
        client_id=config.EDGE_ID,
    )

    try:
        mqtt_client.connect()
        mqtt_client.subscribe_default_topics()
        logger.info(
            "Connected to MQTT broker at %s:%s",
            config.MQTT_BROKER,
            config.MQTT_PORT,
        )
    except Exception:
        logger.exception("Failed to connect to MQTT broker")

    app.state.mqtt_client = mqtt_client

    yield

    logger.info("Edge controller stopping")

    try:
        mqtt_client.disconnect()
        logger.info("Disconnected from MQTT broker")
    except Exception:
        logger.exception("Error while disconnecting MQTT")
