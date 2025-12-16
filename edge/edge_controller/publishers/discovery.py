import requests
from security.auth import headers

DISCOVERY_URL = "https://server/management/devices/discovered/"

def publish_discovered(devices):
    for d in devices:
        requests.post(
            DISCOVERY_URL,
            json=d,
            headers=headers(),
            timeout=3,
        )
