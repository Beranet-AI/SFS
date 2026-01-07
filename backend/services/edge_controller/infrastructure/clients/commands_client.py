import json
from typing import Any
from urllib import request

from ... import config
from ...logging import get_logger

logger = get_logger("CommandsClient")


class CommandsClient:
    def __init__(self) -> None:
        self._endpoint = config.MANAGEMENT_ENDPOINT
        self._base_url = config.MANAGEMENT_COMMANDS_BASE_URL.rstrip("/")

    def send_command_result(self, payload: dict[str, Any]) -> None:
        if self._endpoint == "http":
            self._send_http(payload)
            return

        raise RuntimeError(f"Unsupported management endpoint: {self._endpoint}")

    def _send_http(self, payload: dict[str, Any]) -> None:
        url = f"{self._base_url}/results/"
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        req = request.Request(url, data=body, headers=headers, method="POST")

        logger.info("[COMMANDS] Sending command result to %s", url)
        try:
            with request.urlopen(req, timeout=10) as response:
                status = response.status
                if status >= 400:
                    raise RuntimeError(
                        f"Command result rejected: {status} {response.read().decode('utf-8', errors='ignore')}"
                    )
        except Exception:
            logger.exception("[COMMANDS] Failed to send command result")
            raise
