import json
import paho.mqtt.client as mqtt

from apps.discovery.application.use_cases.ingest_discovery_result import (
    IngestDiscoveryResultUseCase,
)
from apps.commands.application.use_cases.ingest_command_result import (
    IngestCommandResultUseCase,
)
from .topics import discovery_result_topic, command_result_topic


class ManagementMQTTClient:

    def __init__(self, broker_host="localhost", broker_port=1883):
        self.client = mqtt.Client(client_id="management")

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(broker_host, broker_port, 60)

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe("sfs/edge/+/discovery/results")
        client.subscribe("sfs/edge/+/commands/results")
        print("[MANAGEMENT MQTT] Subscribed to discovery & command results")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = json.loads(msg.payload.decode())

        if topic.endswith("/discovery/results"):
            IngestDiscoveryResultUseCase().execute(payload=payload)

        elif topic.endswith("/commands/results"):
            IngestCommandResultUseCase().execute(payload=payload)

    def publish_command(self, *, edge_id: str, command: dict):
        topic = f"sfs/edge/{edge_id}/commands"
        self.client.publish(topic, json.dumps(command))

    def loop_forever(self):
        self.client.loop_forever()
