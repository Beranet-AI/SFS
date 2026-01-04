from apps.commands.domain.entities.command import Command
from apps.commands.domain.enums.command_status import CommandStatus
from apps.commands.domain.enums.command_target_kind import CommandTargetKind
from apps.commands.infrastructure.models.command_model import CommandModel


class CommandMapper:
    @staticmethod
    def to_domain(model: CommandModel) -> Command:
        return Command(
            id=str(model.id),
            command_name=model.command_name,
            target_kind=CommandTargetKind.from_value(model.target_kind),
            target_id=model.target_id,
            edge_node_id=model.edge_node_id,
            payload=model.payload,
            idempotency_key=model.idempotency_key,
            status=CommandStatus.from_value(model.status),
            source=model.source,
            created_by=model.created_by,
            created_at=model.created_at,
            ack_deadline_sec=model.ack_deadline_sec,
            result_deadline_sec=model.result_deadline_sec,
            max_attempts=model.max_attempts,
            acked_at=model.acked_at,
            started_at=model.started_at,
            finished_at=model.finished_at,
            last_error_code=model.last_error_code,
            last_error_message=model.last_error_message,
            last_result=model.last_result,
        )
