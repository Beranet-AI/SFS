import time
from django.db import transaction

from apps.commands.models import CommandModel, CommandAttemptModel
from apps.incidents.application.services.incident_service import IncidentService


class CommandDispatchService:
    """
    Handles dispatch, retry and failure escalation.
    """

    def __init__(self, sender, incident_service: IncidentService):
        self.sender = sender
        self.incident_service = incident_service

    def dispatch(self, *, command_id: str) -> CommandModel:
        command = CommandModel.objects.get(id=command_id)

        with transaction.atomic():
            attempt_no = command.attempts.count() + 1
            attempt = CommandAttemptModel.objects.create(
                command=command,
                attempt_no=attempt_no,
                status="dispatched",
            )
            command.mark_dispatched()
            attempt.dispatched_at = time.time()
            attempt.save(update_fields=["dispatched_at"])

        success, error = self.sender.send(command)

        if success:
            command.mark_acked()
            return command

        if attempt_no >= command.max_attempts:
            command.mark_failed(code="DELIVERY_FAILED", message=error or "")
            self.incident_service.command_failed(command)
            return command

        time.sleep(2)
        return self.dispatch(command_id=command_id)
