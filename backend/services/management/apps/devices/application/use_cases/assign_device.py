from shared.ids.livestock_id import LivestockId
from shared.ids.device_id import DeviceId

class AssignDeviceUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, device_id: DeviceId, livestock_id: LivestockId):
        device = self.repo.get_by_id(device_id)
        device.assign_to_livestock(livestock_id)
        self.repo.save(device)
        return device
