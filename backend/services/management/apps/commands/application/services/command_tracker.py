from __future__ import annotations

from typing import Any
from django.utils import timezone


class CommandTracker:
    """
    ثبت تغییر وضعیت Command/Attempt.
    این نسخه مستقیم با ORM کار می‌کند تا وابستگی به repo interface نداشته باشی.
    """

    def create_attempt(self, *, command, attempt_no: int):
        from apps.commands.infrastructure.models import CommandAttemptModel

        now = timezone.now()
        return CommandAttemptModel.objects.create(
            command=command,
            attempt_no=attempt_no,
            created_at=now,
            status="created",
            debug={},
        )

    def mark_dispatched(self, *, command, attempt) -> None:
        now = timezone.now()
        command.status = "dispatched"
        command.started_at = command.started_at or now
        command.save(update_fields=["status", "started_at"])

        attempt.status = "sent"
        attempt.dispatched_at = now
        attempt.save(update_fields=["status", "dispatched_at"])

    def mark_succeeded(self, *, command, attempt, result: dict[str, Any]) -> None:
        now = timezone.now()
        command.status = "succeeded"
        command.finished_at = now
        command.last_result = result
        command.save(update_fields=["status", "finished_at", "last_result"])

        attempt.status = "result_ok"
        attempt.result_at = now
        attempt.save(update_fields=["status", "result_at"])

    def mark_failed(self, *, command, attempt, error_code: str, error_message: str, result: dict[str, Any] | None = None) -> None:
        now = timezone.now()
        command.status = "failed"
        command.finished_at = now
        command.last_error_code = error_code
        command.last_error_message = error_message
        if result is not None:
            command.last_result = result
        command.save(update_fields=["status", "finished_at", "last_error_code", "last_error_message", "last_result"])

        attempt.status = "result_failed"
        attempt.result_at = now
        attempt.save(update_fields=["status", "result_at"])
