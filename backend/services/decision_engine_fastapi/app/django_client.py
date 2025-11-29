import logging
import time
from typing import Any, Dict

import requests

from .config import settings

logger = logging.getLogger(__name__)

session = requests.Session()

_token_cache: Dict[str, Any] = {
    "access": None,
    "expires_at": 0.0,  # timestamp
}


def get_access_token() -> str:
    """
    گرفتن توکن از Django (با کش ساده در حافظه).
    اگر توکن موجود و هنوز منقضی نشده باشد، همان را استفاده می‌کند.
    """
    now = time.time()

    # اگر توکن موجود است و مثلا تا ۱۰ دقیقه دیگر اعتبار دارد، استفاده کن
    if _token_cache["access"] and _token_cache["expires_at"] > now + 600:
        return _token_cache["access"]

    logger.info("Requesting new access token from Django: %s", settings.django_token_url)

    resp = session.post(
        settings.django_token_url,
        json={
            "username": settings.django_auth_username,
            "password": settings.django_auth_password,
        },
        headers={"Content-Type": "application/json"},
        timeout=10,
    )

    if resp.status_code != 200:
        logger.error(
            "Failed to obtain access token from Django: status=%s body=%s",
            resp.status_code,
            resp.text,
        )
        raise RuntimeError(f"Failed to obtain access token from Django: {resp.status_code}")

    data = resp.json()
    access = data.get("access")
    if not access:
        logger.error("Token response has no 'access' field: %s", data)
        raise RuntimeError("Failed to obtain access token: no 'access' field in response")

    # فعلاً به‌صورت ساده توکن را برای ۵۰ دقیقه معتبر فرض می‌کنیم
    _token_cache["access"] = access
    _token_cache["expires_at"] = now + 50 * 60

    logger.info("Access token obtained successfully from Django")
    return access


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
    token = get_access_token()

    url = f"{settings.django_api_base_url.rstrip('/')}/sensor-readings/"
    logger.info("Posting reading to Django: %s", url)

    resp = session.post(
        url,
        json=reading,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
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
