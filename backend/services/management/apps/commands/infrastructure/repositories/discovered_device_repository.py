from apps.commands.domain.entities.discovered_device import DiscoveredDevice
from apps.commands.domain.repositories.discovered_device_repository import (
    DiscoveredDeviceRepository,
)
from apps.commands.infrastructure.mappers.discovered_device_mapper import (
    DiscoveredDeviceMapper,
)
from apps.commands.infrastructure.models.discovered_device_model import (
    DiscoveredDeviceModel,
    DiscoveredDeviceStatusChoices,
)


class DjangoDiscoveredDeviceRepository(DiscoveredDeviceRepository):
    def get(self, *, discovered_device_id: str) -> DiscoveredDevice:
        device = DiscoveredDeviceModel.objects.get(id=discovered_device_id)
        return DiscoveredDeviceMapper.to_domain(device)

    def list_by_session(self, *, session_id: str) -> list[DiscoveredDevice]:
        devices = DiscoveredDeviceModel.objects.filter(session_id=session_id)
        return [DiscoveredDeviceMapper.to_domain(device) for device in devices]

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
        device, created = DiscoveredDeviceModel.objects.get_or_create(
            session_id=session_id,
            device_id=device_id,
            defaults={
                "device_type": device_type,
                "ip_address": ip_address or "",
                "capabilities": capabilities or {},
                "raw_payload": raw_payload or {},
                "status": DiscoveredDeviceStatusChoices.NEW,
            },
        )

        if not created:
            update_fields = [
                "device_type",
                "ip_address",
                "capabilities",
                "raw_payload",
                "updated_at",
            ]
            device.device_type = device_type
            device.ip_address = ip_address or ""
            device.capabilities = capabilities or {}
            device.raw_payload = raw_payload or {}
            device.save(update_fields=update_fields)

        return DiscoveredDeviceMapper.to_domain(device)

    def mark_registered(
        self, *, discovered_device_id: str, registered_device_id: str
    ) -> DiscoveredDevice:
        device = DiscoveredDeviceModel.objects.get(id=discovered_device_id)
        device.status = DiscoveredDeviceStatusChoices.REGISTERED
        device.registered_device_id = registered_device_id
        device.save(update_fields=["status", "registered_device", "updated_at"])
        return DiscoveredDeviceMapper.to_domain(device)
