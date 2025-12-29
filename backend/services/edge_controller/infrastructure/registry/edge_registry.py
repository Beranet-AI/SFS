class EdgeRegistry:
    """
    Runtime registry of approved / active devices.
    """

    def __init__(self):
        self._approved_devices = set()

    def approve(self, device_id: str):
        self._approved_devices.add(device_id)

    def remove(self, device_id: str):
        self._approved_devices.discard(device_id)

    def is_approved(self, device_id: str) -> bool:
        return device_id in self._approved_devices
