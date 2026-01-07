import os
from typing import Any

import requests
from django.utils import timezone

from apps.commands.infrastructure.models import CommandModel, CommandAttemptModel


class CommandDispatcher:
    """
    مسئول ارسال Command به edge_controller
    """

    def __init__(
        self,
        *,
        edge_base_url: str | None = None,
        edge_execute_path: str | None = None,
        timeout_sec: int | None = None,
    ) -> None:
        self._edge_base_url = (
            edge_base_url
            or os.getenv("EDGE_CONTROLLER_BASE_URL", "http://edge_controller:8003")
        ).rstrip("/")

        self._edge_execute_path = (
            edge_execute_path
            or os.getenv("EDGE_EXECUTE_PATH", "/api/commands")
        )

        self._timeout_sec = timeout_sec or int(
            os.getenv("EDGE_HTTP_TIMEOUT_SEC", "10")
        )

    def _map_command_type(self, command_name: str) -> str:
        return {
            "get_connected_devices": "DISCOVER",
        }.get(command_name, "DISCOVER")

    def dispatch(self, command_id: str) -> None:
        command = CommandModel.objects.get(id=command_id)

        attempt_no = (
            CommandAttemptModel.objects
            .filter(command=command)
            .count() + 1
        )

        attempt = CommandAttemptModel.objects.create(
            command=command,
            attempt_no=attempt_no,
            status="created",
        )

        url = f"{self._edge_base_url}{self._edge_execute_path}"

        payload = {
            "command_id": str(command.id),
            "command_type": self._map_command_type(command.command_name),
            "edge_id": command.target_id,
            "issued_at": timezone.now().isoformat(),
            "payload": command.payload or {},
        }

        try:
            resp = requests.post(url, json=payload, timeout=self._timeout_sec)
            resp.raise_for_status()

            attempt.status = "dispatched"
            attempt.dispatched_at = timezone.now()
            attempt.executor_receipt = resp.text

            command.status = "dispatched"

        except Exception as exc:
            attempt.status = "worker_failed"
            attempt.debug = {"error": str(exc)}

            command.status = "failed"
            command.last_error_message = str(exc)

        attempt.save()
        command.save()
