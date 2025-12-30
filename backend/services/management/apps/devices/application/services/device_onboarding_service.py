from django.db import transaction
from apps.devices.models import DeviceModel


class DeviceOnboardingService:
    """
    Handles promotion of discovery payloads into real devices.
    Discovery is NOT persisted in management.
    """

    @transaction.atomic
    def approve_and_promote(self, payload: dict) -> DeviceModel:
        serial = payload.get("serial")
        if not serial:
            raise ValueError("serial is required")

        device, _ = DeviceModel.objects.get_or_create(
            serial=serial,
            defaults={
                "kind": payload.get("kind", "sensor"),
                "display_name": payload.get("display_name") or serial,
                "farm_id": payload.get("farm_id"),
                "barn_id": payload.get("barn_id"),
                "zone_id": payload.get("zone_id"),
                "livestock_id": payload.get("livestock_id"),
                "metadata": payload.get("metadata") or {},
                "capabilities": payload.get("capabilities") or {},
                "status": "active",
            },
        )

        return device
