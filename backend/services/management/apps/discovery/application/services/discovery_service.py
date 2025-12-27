from django.utils import timezone

from apps.discovery.models import DeviceDiscoveryModel
from apps.devices.models import DeviceModel


class DiscoveryService:
    """
    Application-layer orchestration for device discovery.
    All ORM access lives here.
    """

    # ---------- intake ----------

    def upsert_discovery(self, *, data: dict) -> DeviceDiscoveryModel:
        ext_id = data.get("external_id")
        if not ext_id:
            raise ValueError("external_id required")

        obj, _ = DeviceDiscoveryModel.objects.update_or_create(
            external_id=ext_id,
            defaults={
                "name": data.get("name", "unknown"),
                "device_type": data.get("device_type", "unknown"),
                "protocol": data.get("protocol", "unknown"),
                "role": data.get("role", "sensor"),
                "ip": data.get("ip"),
                "meta": data.get("meta") or {},
                "last_seen": data.get("last_seen"),
            },
        )
        return obj

    # ---------- queries ----------

    def list_pending(self):
        return (
            DeviceDiscoveryModel.objects
            .filter(is_approved=False)
            .order_by("-created_at")
        )

    def get_by_external_id(self, *, external_id: str) -> DeviceDiscoveryModel:
        return DeviceDiscoveryModel.objects.get(external_id=external_id)

    # ---------- approval ----------

    def approve(self, *, discovery: DeviceDiscoveryModel, data: dict) -> DeviceModel:
        device = DeviceModel.objects.create(
            name=data.get("name") or discovery.name,
            device_type=discovery.device_type,
            protocol=discovery.protocol,
            role=discovery.role,
            farm_id=data.get("farm_id") or None,
            barn_id=data.get("barn_id") or None,
            zone_id=data.get("zone_id") or None,
            livestock_id=data.get("livestock_id") or None,
            status=DeviceModel.Status.ACTIVE,
            last_seen=discovery.last_seen,
            meta=discovery.meta,
        )

        discovery.is_approved = True
        discovery.approved_at = timezone.now()
        discovery.save(update_fields=["is_approved", "approved_at"])

        return device
