from apps.devices.infrastructure.clients.monitoring_client import MonitoringClient


class DeviceHealthService:
    """
    Read-only service that queries monitoring / telemetry service
    for device health & metrics.
    """

    def __init__(self, monitoring_client: MonitoringClient):
        self._client = monitoring_client

    def get_health(self, *, device_id: str) -> dict:
        return self._client.get_device_health(device_id=device_id)

    def get_last_metrics(self, *, device_id: str) -> dict:
        return self._client.get_last_metrics(device_id=device_id)
