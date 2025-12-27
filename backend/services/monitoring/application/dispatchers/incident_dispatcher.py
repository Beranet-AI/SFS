from __future__ import annotations

from backend.services.monitoring.domain.enums import IncidentSeverity
from backend.services.monitoring.infrastructure.clients.management_client import ManagementClient


class IncidentDispatcher:
    def __init__(self, management_client: ManagementClient) -> None:
        self.management_client = management_client

    async def device_offline(self, device_id: str, last_seen_at_iso: str) -> None:
        await self.management_client.create_incident(
            title="Device offline",
            device_id=device_id,
            severity=IncidentSeverity.WARNING.value,
            details={"last_seen_at": last_seen_at_iso, "reason": "heartbeat_timeout"},
        )

    async def rule_violation(self, rule_code: str, device_id: str, details: dict) -> None:
        await self.management_client.create_incident(
            title=f"Rule violation: {rule_code}",
            device_id=device_id,
            severity=IncidentSeverity.CRITICAL.value,
            details=details,
        )
