import json
import paho.mqtt.client as mqtt

from application.command.use_cases.listen_commands import (
    ListenCommandsUseCase,
)
from .topics import (
    edge_command_topic,
    discovery_result_topic,
    command_result_topic,
)


class EdgeMQTTClient:

    def __init__(self, *, edge_id: str, broker_host="localhost", broker_port=1883):
        self.edge_id = edge_id
        self.client = mqtt.Client(client_id=f"edge-{edge_id}")

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(broker_host, broker_port, 60)

    def on_connect(self, client, userdata, flags, rc):
        topic = edge_command_topic(self.edge_id)
        client.subscribe(topic)
        print(f"[EDGE MQTT] Subscribed to {topic}")

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        ListenCommandsUseCase().execute(message=message)

    # ---------- publish helpers ----------

    def publish_discovery_result(self, payload: dict):
        topic = discovery_result_topic(self.edge_id)
        self.client.publish(topic, json.dumps(payload))

    def publish_command_result(self, payload: dict):
        topic = command_result_topic(self.edge_id)
        self.client.publish(topic, json.dumps(payload))

    def loop_forever(self):
        self.client.loop_forever()
