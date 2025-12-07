from __future__ import annotations

import logging
from typing import Any, Dict

import requests
from requests import RequestException
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


class DjangoClientError(Exception):
    """Raised when communication with the Django service fails."""


class UnexpectedResponseError(DjangoClientError):
    """Raised when Django returns an unexpected payload."""


def post_sensor_reading(reading: Dict[str, Any]) -> Dict[str, Any]:
    """Send a sensor reading to the Django service."""

    sensor_id = reading.get("sensor_id")
    if not sensor_id:
        raise ValueError("sensor_id is required to post a sensor reading to Django")

    url = _build_url("/sensor-readings/")

    logger.info("Posting reading to Django: %s", url)
    logger.debug("Outgoing reading payload: %s", reading)

    try:
        resp = session.post(
            url,
            json=reading,
            headers=_auth_headers(include_json=True),
            timeout=10,
        )
    except RequestException as exc:
        raise DjangoClientError(f"Failed to POST reading to Django: {exc}") from exc

    if resp.status_code not in (200, 201):
        logger.error(
            "Error posting to Django endpoint=sensor-readings/ status=%s body=%s",
            resp.status_code,
            resp.text,
        )
        resp.raise_for_status()

    try:
        return resp.json()
    except ValueError as exc:
        raise UnexpectedResponseError("Received non-JSON response from Django") from exc


def _auth_headers(include_json: bool = False) -> Dict[str, str]:
    token = settings.django_service_token.get_secret_value()
    headers = {
        "Authorization": f"Token {token}",
        "Accept": "application/json",
    }
    if include_json:
        headers["Content-Type"] = "application/json"
    return headers


def _build_url(path: str) -> str:
    normalized_path = path if path.startswith("/") else f"/{path}"
    return f"{settings.api_base_url}{normalized_path}"


def sensor_exists(sensor_id: int) -> bool:
    """Check whether a sensor exists before attempting to post readings."""

    url = _build_url(f"/sensors/{sensor_id}/")
    try:
        resp = session.get(url, headers=_auth_headers(), timeout=5)
    except RequestException as exc:
        raise DjangoClientError(f"Failed to verify sensor {sensor_id} existence: {exc}") from exc

    if resp.status_code == 404:
        logger.warning("Sensor %s not found in Django (url=%s)", sensor_id, url)
        return False

    try:
        resp.raise_for_status()
    except Exception as exc:  # requests.HTTPError is fine but broader keeps context
        logger.error(
            "Error checking sensor existence id=%s status=%s body=%s",
            sensor_id,
            resp.status_code,
            resp.text,
        )
        raise DjangoClientError(
            f"Failed to verify sensor {sensor_id} existence: {resp.status_code}"
        ) from exc

    return True
