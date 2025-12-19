from apps.devices.domain.entities.device import Device
from apps.devices.infrastructure.models.device_model import DeviceModel
from apps.devices.domain.enums.device_status import DeviceStatus
from shared.ids.device_id import DeviceId
from shared.ids.livestock_id import LivestockId
from shared.enums.device_type import DeviceType

class DjangoDeviceRepository:

    def get_by_id(self, device_id: DeviceId) -> Device:
        obj = DeviceModel.objects.get(id=device_id)
        return Device(
            id=DeviceId(str(obj.id)),
            serial=obj.serial,
            device_type=DeviceType(obj.device_type),
            status=DeviceStatus(obj.status),
            assigned_livestock_id=LivestockId(obj.assigned_livestock_id)
            if obj.assigned_livestock_id else None
        )

    def save(self, device: Device) -> None:
        DeviceModel.objects.update_or_create(
            id=device.id,
            defaults={
                "serial": device.serial,
                "device_type": device.device_type.value,
                "status": device.status.value,
                "assigned_livestock_id": (
                    str(device.assigned_livestock_id)
                    if device.assigned_livestock_id else None
                ),
            },
        )
