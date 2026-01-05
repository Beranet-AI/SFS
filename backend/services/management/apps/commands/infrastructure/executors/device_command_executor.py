from apps.commands.infrastructure.clients.edge_controller_client import (
    EdgeControllerClient,
)


class DeviceCommandExecutor:
    def __init__(self, *, edge_client: EdgeControllerClient) -> None:
        self._edge_client = edge_client

    def execute(self, *, edge_id: str, command: dict) -> None:
        self._edge_client.publish_command(edge_id=edge_id, command=command)
