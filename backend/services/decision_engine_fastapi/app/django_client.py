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

    url = f"{settings.django_api_base_url.rstrip('/')}/sensor-readings/"
    logger.info("Posting reading to Django: %s", url)

    headers = {
        "Authorization": f"Token {settings.django_service_token}",
        "Content-Type": "application/json",
    }

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
