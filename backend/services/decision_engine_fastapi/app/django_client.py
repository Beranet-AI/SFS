import logging
from typing import Any, Dict

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import settings

logger = logging.getLogger(__name__)

session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=(502, 503, 504),
    allowed_methods=frozenset(["GET", "POST"]),
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)


def post_sensor_reading(reading: Dict[str, Any]) -> Dict[str, Any]:
    """
    ارسال یک SensorReading به Django
    reading باید شبیه همین باشد:
    {
        "sensor_id": 1,
        "value": 25.7,
        "quality": "good",
        "raw_payload": {...}
    }
    """
    if "sensor_id" not in reading or not reading.get("sensor_id"):
        raise ValueError("sensor_id is required to post a sensor reading to Django")

    url = f"{settings.DJANGO_API_BASE_URL.rstrip('/')}/sensor-readings/"
    #sensor_id = reading["sensor_id"]
    #url = f"{settings.DJANGO_API_BASE_URL.rstrip('/')}/sensors/{sensor_id}/"

    # همین‌جا print کن:
    print("BASE URL =", settings.DJANGO_API_BASE_URL)
    print("Sensor URL =", url)

    logger.info("Posting reading to Django: %s", url)
    logger.info("Outgoing reading payload: %s", reading)

    headers = _auth_headers(include_json=True)
    logger.debug(
        "Using Django request headers: %s",
        {"Authorization": "Token ***", "Content-Type": headers.get("Content-Type")},
    )

    resp = session.post(
        url,
        json=reading,
        headers=headers,
        timeout=10,
    )

    if resp.status_code not in (200, 201):
        logger.error(
            "Error posting to Django endpoint=sensor-readings/ status=%s body=%s",
            resp.status_code,
            resp.text,
        )
        resp.raise_for_status()

    return resp.json()


def _auth_headers(include_json: bool = False) -> Dict[str, str]:
    headers = {
        "Authorization": f"Token {settings.DJANGO_SERVICE_TOKEN}",
        "Accept": "application/json",    #
    }
    if include_json:
        headers["Content-Type"] = "application/json"
    return headers


def sensor_exists(sensor_id: int) -> bool:
    """Check whether a sensor exists before attempting to post readings."""
    url = f"{settings.DJANGO_API_BASE_URL.rstrip('/')}/sensors/{sensor_id}/"
    resp = session.get(url, headers=_auth_headers(), timeout=5)
    if resp.status_code == 404:
        logger.error("Sensor %s not found in Django (url=%s)", sensor_id, url)
        return False
    try:
        resp.raise_for_status()
    except Exception:
        logger.error(
            "Error checking sensor existence id=%s status=%s body=%s",
            sensor_id,
            resp.status_code,
            resp.text,
        )
        raise
    return True
