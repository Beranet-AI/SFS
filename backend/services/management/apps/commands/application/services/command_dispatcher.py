import os
import requests
from django.utils import timezone

from apps.commands.infrastructure.models import (
    CommandModel,
    CommandAttemptModel,
)


class CommandDispatcher:
    """
    مسئول Dispatch یک Command به edge_controller
    """

    def __init__(
        self,
        *,
        edge_base_url: str | None = None,
        edge_execute_path: str | None = None,
        timeout_sec: int | None = None,
    ) -> None:
        self.edge_base_url = (
            edge_base_url
            or os.getenv("EDGE_CONTROLLER_BASE_URL", "http://edge_controller:8003")
        ).rstrip("/")

        self.edge_execute_path = (
            edge_execute_path
            or os.getenv("EDGE_EXECUTE_PATH", "/api/commands")
        )

        self.timeout_sec = (
            timeout_sec
            if timeout_sec is not None
            else int(os.getenv("EDGE_HTTP_TIMEOUT_SEC", "10"))
        )

    def dispatch(self, command_id):
        command = CommandModel.objects.get(id=command_id)

        attempt_no = command.attempts.count() + 1
        attempt = CommandAttemptModel.objects.create(
            command=command,
            attempt_no=attempt_no,
            status="dispatching",
        )

        url = f"{self.edge_base_url}{self.edge_execute_path}"

        body = {
            "command_id": str(command.id),
            "command_type": self._map_command_name(command.command_name),
            "edge_id": command.target_id,
            "issued_at": timezone.now().isoformat(),
            "payload": command.payload or {},
        }

        try:
            resp = requests.post(url, json=body, timeout=self.timeout_sec)
            resp.raise_for_status()

            attempt.status = "dispatched"
            attempt.dispatched_at = timezone.now()
            attempt.executor_receipt = resp.text
            attempt.save()

            command.status = "dispatched"
            command.save(update_fields=["status"])

        except Exception as exc:
            attempt.status = "worker_failed"
            attempt.debug = {"error": str(exc)}
            attempt.save()

            command.status = "failed"
            command.last_error_message = str(exc)
            command.save(update_fields=["status", "last_error_message"])

            raise

    def _map_command_name(self, name: str) -> str:
        return {
            "get_connected_devices": "DISCOVER",
        }.get(name, name.upper())
