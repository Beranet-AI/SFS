from __future__ import annotations

from backend.services.monitoring.infrastructure.clients.command_client import CommandClient


class CommandDispatcher:
    """
    Sends commands to edge_controller (actuators, fans, vents, ozone, etc.)
    For now: fire-and-forget. Later we add Command Status & Retry Policy (مرحله 3).
    """

    def __init__(self, command_client: CommandClient) -> None:
        self.command_client = command_client

    async def send_command(self, device_id: str, command: str, params: dict | None = None) -> None:
        await self.command_client.send_command(
            device_id=device_id,
            command=command,
            params=params or {},
        )
