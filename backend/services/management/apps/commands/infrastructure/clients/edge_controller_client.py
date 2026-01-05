import json

import paho.mqtt.client as mqtt

from apps.commands.application.use_cases.receive_result.input_dto import (
    ReceiveResultInputDTO,
)
from apps.commands.application.use_cases.receive_result.use_case import (
    ReceiveResultUseCase,
)
from apps.commands.infrastructure.repositories.django_command_repository import (
    DjangoCommandRepository,
)
from .topics import command_result_topic, edge_command_topic


class EdgeControllerClient:
    """
    MQTT client for communicating with edge_controller.
    Responsibilities:
    - publish commands
    - receive command execution results
    """

    def __init__(self, broker_host: str = "localhost", broker_port: int = 1883):
        self.client = mqtt.Client(client_id="management")

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(broker_host, broker_port, 60)

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(command_result_topic("+"))

    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode())

        dto = ReceiveResultInputDTO(
            command_id=str(payload["command_id"]),
            attempt_no=payload["attempt_no"],
            status=payload["status"],
            result=payload.get("result", {}),
            error_code=payload.get("error_code", ""),
            error_message=payload.get("error_message", ""),
            meta=payload.get("meta", {}),
        )

        ReceiveResultUseCase(
            command_repository=DjangoCommandRepository(),
        ).execute(dto)

    def publish_command(self, *, edge_id: str, command: dict) -> None:
        topic = edge_command_topic(edge_id)
        self.client.publish(topic, json.dumps(command))

    def loop_forever(self) -> None:
        self.client.loop_forever()
