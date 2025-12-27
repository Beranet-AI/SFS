from django.db import transaction
from apps.devices.models import DeviceModel
from apps.discovery.models import DeviceDiscoveryModel


class DeviceOnboardingService:
    """
    Handles promotion of discovered devices into real devices.
    """

    @transaction.atomic
    def approve_and_promote(self, discovery_id: int) -> DeviceModel:
        discovery = DeviceDiscoveryModel.objects.select_for_update().get(
            id=discovery_id
        )

        if discovery.status == "approved":
            # idempotent behavior
            return DeviceModel.objects.get(serial=discovery.serial)

        device, _ = DeviceModel.objects.get_or_create(
            serial=discovery.serial,
            defaults={
                "kind": discovery.device_type,
                "display_name": discovery.display_name or discovery.serial,
                "farm_id": discovery.farm_id,
                "livestock_id": discovery.livestock_id,
                "metadata": discovery.metadata or {},
                "status": "active",
            },
        )

        discovery.status = "approved"
        discovery.save(update_fields=["status"])

        return device
