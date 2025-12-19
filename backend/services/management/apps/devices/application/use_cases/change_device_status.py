class ChangeDeviceStatusUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, device_id, status):
        device = self.repo.get_by_id(device_id)
        device.change_status(status)
        self.repo.save(device)
        return device
