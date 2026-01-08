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

    def send_command_result(
        self,
        *,
        command_id: str,
        attempt_no: int,
        status: str,
        result: dict | None = None,
        error_code: str = "",
        error_message: str = "",
        meta: dict | None = None,
    ) -> None:
        payload = {
            "command_id": command_id,
            "attempt_no": attempt_no,
            "status": status,
            "result": result or {},
            "error_code": error_code,
            "error_message": error_message,
            "meta": meta or {},
        }

        if self._endpoint == "http":
            self._send_http(payload)
            return

        raise RuntimeError(f"Unsupported management endpoint: {self._endpoint}")

    def _send_http(self, payload: dict[str, Any]) -> None:
        url = f"{self._base_url}/results/"
        body = json.dumps(payload).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
        }

        req = request.Request(
            url=url,
            data=body,
            headers=headers,
            method="POST",
        )

        logger.info("[COMMANDS] Sending command result to %s", url)

        try:
            with request.urlopen(req, timeout=10) as response:
                if response.status >= 400:
                    raise RuntimeError(
                        f"Command result rejected: {response.status}"
                    )
        except Exception:
            logger.exception("[COMMANDS] Failed to send command result")
            raise
