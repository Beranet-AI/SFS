import requests

MANAGEMENT_URL = "http://management:8000"

def is_device_allowed(device_id: str) -> bool:
    res = requests.get(
        f"{MANAGEMENT_URL}/devices/{device_id}/validate/",
        timeout=2,
    )
    return res.ok and res.json().get("approved", False)
