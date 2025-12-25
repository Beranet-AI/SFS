from datetime import datetime, timezone, timedelta
from apps.monitoring.infrastructure.clients.management_client import ManagementClient


class HeartbeatWatcher:
    def __init__(self):
        self.mgmt = ManagementClient()

    def run(self):
        devices = self.mgmt.list_devices()

        now = datetime.now(timezone.utc)

        for d in devices:
            if not d["last_seen_at"]:
                continue

            last_seen = datetime.fromisoformat(d["last_seen_at"])
            if now - last_seen > timedelta(seconds=d["heartbeat_timeout_sec"]):
                self.mgmt.mark_device_offline(d["device_serial"])
                self.mgmt.create_incident({
                    "code": "DEVICE_OFFLINE",
                    "severity": "high",
                    "title": "Device offline",
                    "device_serial": d["device_serial"],
                })
