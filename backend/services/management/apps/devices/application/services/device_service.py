from typing import Any

from apps.devices.models import DeviceModel, DeviceStatus


class DeviceService:
    """
    Application service responsible for the full Device lifecycle:
    - discovery upsert
    - approval / activation
    - assignment
    - status changes
    """

    # -------------------------
    # Queries
    # -------------------------

    def get_by_id(self, *, device_id: str) -> DeviceModel:
        return DeviceModel.objects.get(id=device_id)

    def get_by_serial(self, *, serial: str) -> DeviceModel:
        return DeviceModel.objects.get(serial=serial)

    # -------------------------
    # Registration / discovery
    # -------------------------

    def register_or_update(
        self,
        *,
        serial: str,
        kind: str,
        display_name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DeviceModel:
        obj, _ = DeviceModel.objects.get_or_create(
            serial=serial,
            defaults={
                "kind": kind,
                "display_name": display_name or "",
                "metadata": metadata or {},
                "status": DeviceStatus.DISCOVERED,
            },
        )

        # update mutable fields
        obj.kind = kind
        if display_name is not None:
            obj.display_name = display_name
        if metadata is not None:
            obj.metadata = metadata

        obj.save(update_fields=["kind", "display_name", "metadata", "updated_at"])
        return obj

    # -------------------------
    # Activation / lifecycle
    # -------------------------

    def activate(self, *, device: DeviceModel) -> None:
        device.change_status(DeviceStatus.ACTIVE)

    def deactivate(self, *, device: DeviceModel) -> None:
        device.change_status(DeviceStatus.INACTIVE)

    def disable(self, *, device: DeviceModel) -> None:
        device.change_status(DeviceStatus.DISABLED)

    # -------------------------
    # Assignment
    # -------------------------

    def assign(
        self,
        *,
        device: DeviceModel,
        farm_id: str | None = None,
        barn_id: str | None = None,
        zone_id: str | None = None,
        livestock_id: str | None = None,
    ) -> None:
        device.assign(
            farm_id=farm_id,
            barn_id=barn_id,
            zone_id=zone_id,
            livestock_id=livestock_id,
        )

    # -------------------------
    # Telemetry / heartbeat
    # -------------------------

    def mark_seen(self, *, device: DeviceModel) -> None:
        device.mark_seen()
