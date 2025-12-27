import uuid
from apps.commands.infrastructure.mqtt.client import ManagementMQTTClient


class RequestEdgeScanUseCase:

    def execute(self, *, edge_id: str):
        request_id = str(uuid.uuid4())

        command = {
            "command": "scan_network",
            "edge_id": edge_id,
            "request_id": request_id,
        }

        mqtt = ManagementMQTTClient()
        mqtt.publish_command(edge_id=edge_id, command=command)

        return request_id
