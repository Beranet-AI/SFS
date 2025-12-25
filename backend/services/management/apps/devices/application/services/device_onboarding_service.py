from dataclasses import dataclass
from django.db import transaction
from django.utils import timezone

from apps.devices.infrastructure.models.device_discovery_model import (
    DeviceDiscoveryModel,
    DiscoveryStatus,
)
from apps.devices.infrastructure.models.device_model import DeviceModel, DeviceStatus


@dataclass(frozen=True)
class ApprovePayload:
    """
    Operator-provided info when approving a discovery.
    """

    name: str = ""
    farm_id: str = ""
    barn_id: str = ""
    zone_id: str = ""
    livestock_id: str = ""
    device_type: str = ""  # optional override if needed
    protocol: str = ""
    metadata: dict | None = None


class DeviceOnboardingService:
    @transaction.atomic
    def upsert_discovery(self, payload: dict) -> DeviceDiscoveryModel:
        """
        Called by edge_controller -> management.
        Stores (or updates) pending discovered device.
        """
        serial_number = payload.get("serial_number") or payload.get("serial") or ""
        device_type = payload.get("device_type") or payload.get("type") or ""
        if not serial_number or not device_type:
            raise ValueError("serial_number and device_type are required")

        obj, _ = DeviceDiscoveryModel.objects.get_or_create(
            serial_number=serial_number,
            device_type=device_type,
            defaults={},
        )

        obj.protocol = payload.get("protocol", obj.protocol)
        obj.ip_address = payload.get("ip_address") or payload.get("ip")
        obj.firmware_version = payload.get("firmware_version", obj.firmware_version)
        obj.last_payload = payload
        obj.last_seen_at = timezone.now()

        # if already approved/rejected, we still update last_seen/payload but keep status
        obj.save()
        return obj

    @transaction.atomic
    def approve(self, discovery_id: int, approve: ApprovePayload) -> DeviceModel:
        discovery = DeviceDiscoveryModel.objects.select_for_update().get(id=discovery_id)

        # promote to DeviceModel
        device_type = approve.device_type or discovery.device_type
        protocol = approve.protocol or discovery.protocol

        device, _created = DeviceModel.objects.get_or_create(
            serial_number=discovery.serial_number,
            defaults={
                "device_type": device_type,
            },
        )

        # update fields
        device.device_type = device_type
        device.protocol = protocol
        device.ip_address = discovery.ip_address
        device.firmware_version = discovery.firmware_version

        device.name = approve.name or device.name
        device.farm_id = approve.farm_id or device.farm_id
        device.barn_id = approve.barn_id or device.barn_id
        device.zone_id = approve.zone_id or device.zone_id
        device.livestock_id = approve.livestock_id or device.livestock_id

        if approve.metadata:
            device.metadata = {**(device.metadata or {}), **approve.metadata}

        device.approved_at = device.approved_at or timezone.now()
        device.status = DeviceStatus.ACTIVE
        device.last_seen_at = timezone.now()
        device.save()

        discovery.status = DiscoveryStatus.APPROVED
        discovery.save(update_fields=["status", "updated_at"])

        return device

    @transaction.atomic
    def reject(self, discovery_id: int, note: str = "") -> DeviceDiscoveryModel:
        discovery = DeviceDiscoveryModel.objects.select_for_update().get(id=discovery_id)
        discovery.status = DiscoveryStatus.REJECTED
        discovery.note = note or discovery.note
        discovery.save(update_fields=["status", "note", "updated_at"])
        return discovery
