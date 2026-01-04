from apps.commands.domain.entities.command_attempt import CommandAttempt
from apps.commands.infrastructure.models.command_attempt_model import CommandAttemptModel


class CommandAttemptMapper:
    @staticmethod
    def to_domain(model: CommandAttemptModel) -> CommandAttempt:
        return CommandAttempt(
            id=str(model.id),
            command_id=str(model.command_id),
            attempt_no=model.attempt_no,
            status=model.status,
            created_at=model.created_at,
            dispatched_at=model.dispatched_at,
            acked_at=model.acked_at,
            result_at=model.result_at,
            executor_receipt=model.executor_receipt,
            debug=model.debug,
        )
