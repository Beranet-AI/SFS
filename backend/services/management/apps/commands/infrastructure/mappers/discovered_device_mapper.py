from apps.commands.domain.entities.discovered_device import DiscoveredDevice
from apps.commands.domain.enums.discovered_device_status import (
    DiscoveredDeviceStatus,
)
from apps.commands.infrastructure.models.discovered_device_model import (
    DiscoveredDeviceModel,
)


class DiscoveredDeviceMapper:
    @staticmethod
    def to_domain(model: DiscoveredDeviceModel) -> DiscoveredDevice:
        return DiscoveredDevice(
            id=str(model.id),
            session_id=str(model.session_id),
            device_id=model.device_id,
            device_type=model.device_type,
            ip_address=model.ip_address or None,
            status=DiscoveredDeviceStatus.from_value(model.status),
            capabilities=model.capabilities or {},
            raw_payload=model.raw_payload or {},
            registered_device_id=str(model.registered_device_id)
            if model.registered_device_id
            else None,
        )
