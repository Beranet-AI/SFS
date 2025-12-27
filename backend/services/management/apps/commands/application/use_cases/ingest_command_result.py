from apps.commands.models import CommandModel


class IngestCommandResultUseCase:

    def execute(self, *, payload: dict):
        CommandModel.objects.filter(
            command_id=payload["command_id"]
        ).update(
            status=payload["status"]
        )
