from datetime import datetime, timezone
from apps.monitoring.infrastructure.clients.management_client import ManagementClient


class DeviceHealthService:
    def __init__(self):
        self.mgmt = ManagementClient()

    async def on_heartbeat(self, payload: dict):
        self.mgmt.update_device_health(
            device_serial=payload["device_serial"],
            last_seen_at=payload.get("ts"),
            status="online",
        )
