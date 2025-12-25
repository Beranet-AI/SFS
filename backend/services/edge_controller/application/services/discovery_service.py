from typing import Dict, Any
from edge_controller.core.config import settings
from edge_controller.infrastructure.clients.management_client import ManagementClient


class DiscoveryService:
    def __init__(self, mgmt: ManagementClient):
        self.mgmt = mgmt

    def on_seen(self, device: Dict[str, Any]) -> None:
        if not settings.ENABLE_DEVICE_DISCOVERY:
            return
        self.mgmt.upsert_discovery(device)
