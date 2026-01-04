from django.utils import timezone

from apps.commands.domain.entities.command_attempt import CommandAttempt
from apps.commands.domain.repositories.command_attempt_repository import (
    CommandAttemptRepository,
)
from apps.commands.infrastructure.mappers.command_attempt_mapper import (
    CommandAttemptMapper,
)
from apps.commands.infrastructure.models.command_attempt_model import CommandAttemptModel
from apps.commands.infrastructure.models.command_model import CommandModel


class DjangoCommandAttemptRepository(CommandAttemptRepository):
    def record_ack(
        self,
        *,
        command_id: str,
        attempt_no: int,
        executor_receipt: str | None = None,
        meta: dict | None = None,
    ) -> CommandAttempt:
        command = CommandModel.objects.get(id=command_id)
        attempt, _ = CommandAttemptModel.objects.get_or_create(
            command=command,
            attempt_no=attempt_no,
            defaults={"status": "sent", "dispatched_at": timezone.now()},
        )
        attempt.executor_receipt = executor_receipt or ""
        attempt.acked_at = timezone.now()
        attempt.status = "acked"
        attempt.debug = {**(attempt.debug or {}), "ack_meta": meta or {}}
        attempt.save(update_fields=["executor_receipt", "acked_at", "status", "debug"])
        return CommandAttemptMapper.to_domain(attempt)

    def record_result(
        self,
        *,
        command_id: str,
        attempt_no: int,
        status: str,
        result: dict | None = None,
        error_code: str = "",
        error_message: str = "",
        meta: dict | None = None,
    ) -> CommandAttempt:
        command = CommandModel.objects.get(id=command_id)
        attempt, _ = CommandAttemptModel.objects.get_or_create(
            command=command,
            attempt_no=attempt_no,
            defaults={"status": "sent", "dispatched_at": timezone.now()},
        )

        attempt.result_at = timezone.now()
        attempt.debug = {**(attempt.debug or {}), "result_meta": meta or {}}
        attempt.status = status
        attempt.save(update_fields=["result_at", "status", "debug"])
        return CommandAttemptMapper.to_domain(attempt)
