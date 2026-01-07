# apps/commands/infrastructure/clients/edge_controller_client.py

from typing import Any

import requests

from apps.commands.domain.exceptions.command_execution_error import (
    CommandExecutionError,
)


class EdgeControllerClient:
    """
    HTTP client for communicating with edge_controller service.
    Management MUST NOT talk to MQTT directly.
    """

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or "http://edge_controller:8003"

    def discover_network(self) -> dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/commands/discover",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def send_command(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/commands/execute",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def publish_command(self, *, edge_id: str, command: dict[str, Any]) -> dict[str, Any]:
        payload = {**command, "edge_id": edge_id}
        try:
            return self.send_command(payload)
        except requests.RequestException as exc:
            raise CommandExecutionError(
                f"Failed to reach edge controller at {self.base_url}"
            ) from exc
