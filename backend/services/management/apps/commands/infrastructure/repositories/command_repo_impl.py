from django.utils import timezone

from apps.commands.domain.entities.command import Command
from apps.commands.domain.enums.command_status import CommandStatus
from apps.commands.domain.repositories.command_repository import CommandRepository
from apps.commands.infrastructure.mappers.command_mapper import CommandMapper
from apps.commands.infrastructure.models.command_model import (
    CommandModel,
    CommandStatusChoices,
)


class DjangoCommandRepository(CommandRepository):
    def create(self, *, data: dict, created_by: str) -> Command:
        command = CommandModel.objects.create(
            **data,
            status=CommandStatusChoices.PENDING,
            created_by=created_by or "manual",
        )
        return CommandMapper.to_domain(command)

    def get(self, *, command_id: str) -> Command:
        command = CommandModel.objects.get(id=command_id)
        return CommandMapper.to_domain(command)

    def mark_acked(self, *, command_id: str, meta: dict | None = None) -> Command:
        command = CommandModel.objects.get(id=command_id)
        command.mark_acked(meta=meta)
        return CommandMapper.to_domain(command)

    def mark_dispatched(self, *, command_id: str) -> Command:
        command = CommandModel.objects.get(id=command_id)
        command.mark_dispatched()
        return CommandMapper.to_domain(command)

    def mark_result(
        self,
        *,
        command_id: str,
        status: CommandStatus,
        result: dict | None = None,
        error_code: str = "",
        error_message: str = "",
    ) -> Command:
        command = CommandModel.objects.get(id=command_id)

        if status == CommandStatus.SUCCEEDED:
            command.mark_succeeded(result=result)
        elif status == CommandStatus.FAILED:
            command.mark_failed(code=error_code, message=error_message, result=result)
        else:
            command.status = status.value
            command.finished_at = timezone.now()
            command.last_result = result or {}
            command.last_error_code = error_code or ""
            command.last_error_message = error_message or ""
            command.save(
                update_fields=[
                    "status",
                    "finished_at",
                    "last_result",
                    "last_error_code",
                    "last_error_message",
                ]
            )

        return CommandMapper.to_domain(command)
