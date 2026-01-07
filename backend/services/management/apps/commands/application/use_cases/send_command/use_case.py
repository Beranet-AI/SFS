from __future__ import annotations

from apps.commands.application.services.command_dispatcher import CommandDispatcher
from apps.commands.application.services.command_tracker import CommandTracker
from apps.commands.application.use_cases.send_command.input_dto import SendCommandInputDTO
from apps.commands.application.use_cases.send_command.output_dto import SendCommandOutputDTO


class SendCommandUseCase:
    def __init__(
        self,
        *,
        dispatcher: CommandDispatcher,
        tracker: CommandTracker,
    ) -> None:
        self._dispatcher = dispatcher
        self._tracker = tracker

    def execute(self, *, input_dto: SendCommandInputDTO) -> SendCommandOutputDTO:
        from apps.commands.infrastructure.models import CommandModel

        cmd = CommandModel.objects.create(
            command_name=input_dto.command_name,
            target_kind=input_dto.target_kind,
            target_id=input_dto.target_id,
            payload=input_dto.payload or {},
            idempotency_key=input_dto.idempotency_key,
            source=input_dto.source,
            created_by=input_dto.created_by,
            ack_deadline_sec=input_dto.ack_deadline_sec,
            result_deadline_sec=input_dto.result_deadline_sec,
            max_attempts=input_dto.max_attempts,
        )

        # create attempt
        attempt_no = 1
        attempt = self._tracker.create_attempt(command=cmd, attempt_no=attempt_no)
        self._tracker.mark_dispatched(command=cmd, attempt=attempt)

        # dispatch
        edge_json = self._dispatcher.dispatch_to_edge(
            command_id=str(cmd.id),
            command_name=cmd.command_name,
            edge_id=str(cmd.target_id),
            payload=cmd.payload,
        )

        edge_status = str(edge_json.get("status", "")).upper()
        if edge_status == "COMPLETED":
            self._tracker.mark_succeeded(command=cmd, attempt=attempt, result=edge_json)
        else:
            self._tracker.mark_failed(
                command=cmd,
                attempt=attempt,
                error_code=str(edge_json.get("error_code") or "EDGE_FAILED"),
                error_message=str(edge_json.get("error_message") or edge_json),
                result=edge_json,
            )

        cmd.refresh_from_db()
        return SendCommandOutputDTO(command_id=str(cmd.id), status=str(cmd.status), last_result=cmd.last_result)
