from typing import Protocol

from apps.commands.domain.entities.discovered_device import DiscoveredDevice


class DiscoveredDeviceRepository(Protocol):
    def get(self, *, discovered_device_id: str) -> DiscoveredDevice:
        ...

    def list_by_session(self, *, session_id: str) -> list[DiscoveredDevice]:
        ...

    def upsert(
        self,
        *,
        session_id: str,
        device_id: str,
        device_type: str,
        ip_address: str | None,
        capabilities: dict,
        raw_payload: dict,
    ) -> DiscoveredDevice:
        ...

    def mark_registered(
        self, *, discovered_device_id: str, registered_device_id: str
    ) -> DiscoveredDevice:
        ...
