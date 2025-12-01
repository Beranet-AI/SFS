import logging
import time
from typing import Any, Dict, Optional

import jwt
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

_token_cache: Dict[str, Any] = {
    "access": None,
    "expires_at": 0.0,  # timestamp
}


def _extract_expiry(token: str) -> Optional[float]:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp = payload.get("exp")
        return float(exp) if exp is not None else None
    except jwt.PyJWTError as exc:
        logger.warning("Could not decode JWT expiry: %s", exc)
        return None


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

    expires_at = _extract_expiry(access)
    if expires_at:
        _token_cache["expires_at"] = expires_at
    else:
        # fallback: SimpleJWT پیش‌فرض 30 دقیقه است
        _token_cache["expires_at"] = now + 25 * 60

    _token_cache["access"] = access

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
    if "sensor_id" not in reading or not reading.get("sensor_id"):
        raise ValueError("sensor_id is required to post a sensor reading to Django")

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
