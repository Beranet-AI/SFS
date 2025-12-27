from dataclasses import dataclass
from backend.shared.ids.device_id import DeviceId
from backend.shared.ids.livestock_id import LivestockId
from backend.shared.enums.device_type import DeviceType
from apps.devices.domain.enums.device_status import DeviceStatus

@dataclass
class Device:
    id: DeviceId
    serial: str
    device_type: DeviceType
    status: DeviceStatus
    assigned_livestock_id: LivestockId | None = None

    def assign_to_livestock(self, livestock_id: LivestockId):
        self.assigned_livestock_id = livestock_id

    def unassign(self):
        self.assigned_livestock_id = None

    def change_status(self, status: DeviceStatus):
        self.status = status
