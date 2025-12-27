import httpx


class MonitoringClient:
    """
    Infrastructure client for communicating with Monitoring service.
    """

    BASE_URL = "http://sfs-monitoring:8002"

    def get_device_health(self, device_id: str) -> dict:
        response = httpx.get(
            f"{self.BASE_URL}/devices/{device_id}/health",
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
