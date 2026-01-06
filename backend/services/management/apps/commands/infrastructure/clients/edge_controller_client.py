# apps/commands/infrastructure/clients/edge_controller_client.py

import requests
from typing import Any


class EdgeControllerClient:
    """
    HTTP client for communicating with edge_controller service.
    Management MUST NOT talk to MQTT directly.
    """

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or "http://edge-controller:8003"

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
