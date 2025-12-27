from __future__ import annotations

import httpx


class CommandClient:
    """
    Talks to edge_controller to control actuators.
    In "مرحله Command Status & Retry Policy" this becomes stateful.
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    async def send_command(self, device_id: str, command: str, params: dict) -> None:
        url = f"{self.base_url}/commands/send"
        payload = {"device_id": device_id, "command": command, "params": params}
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                await client.post(url, json=payload)
            except Exception:
                return
