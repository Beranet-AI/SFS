from django.utils import timezone

from apps.commands.models import (
    CommandModel,
    CommandAttemptModel,
    CommandStatus,
)


class CommandApiService:
    """
    Application-layer orchestration for Commands API.
    """

    def create_command(self, *, data: dict, created_by: str):
        return CommandModel.objects.create(
            **data,
            status=CommandStatus.PENDING,
            created_by=created_by or "manual",
        )

    def get_command(self, *, command_id: str) -> CommandModel:
        return CommandModel.objects.get(id=command_id)

    def ack_command(self, *, data: dict):
        cmd = CommandModel.objects.get(id=data["command_id"])

        attempt, _ = CommandAttemptModel.objects.get_or_create(
            command=cmd,
            attempt_no=data["attempt_no"],
            defaults={"status": "sent", "dispatched_at": timezone.now()},
        )

        attempt.executor_receipt = data.get("executor_receipt", "")
        attempt.acked_at = timezone.now()
        attempt.status = "acked"
        attempt.debug = {**(attempt.debug or {}), "ack_meta": data.get("meta", {})}
        attempt.save(update_fields=["executor_receipt", "acked_at", "status", "debug"])

        cmd.mark_acked(meta=data.get("meta", {}))

    def report_result(self, *, data: dict):
        cmd = CommandModel.objects.get(id=data["command_id"])

        attempt, _ = CommandAttemptModel.objects.get_or_create(
            command=cmd,
            attempt_no=data["attempt_no"],
            defaults={"status": "sent", "dispatched_at": timezone.now()},
        )

        attempt.result_at = timezone.now()
        attempt.debug = {**(attempt.debug or {}), "result_meta": data.get("meta", {})}

        final_status = data["status"]

        if final_status == CommandStatus.SUCCEEDED:
            attempt.status = "succeeded"
            attempt.save(update_fields=["result_at", "status", "debug"])
            cmd.mark_succeeded(result=data.get("result", {}))

        elif final_status == CommandStatus.FAILED:
            attempt.status = "failed"
            attempt.save(update_fields=["result_at", "status", "debug"])
            cmd.mark_failed(
                code=data.get("error_code", ""),
                message=data.get("error_message", ""),
                result=data.get("result", {}),
            )

        else:
            attempt.status = final_status
            attempt.save(update_fields=["result_at", "status", "debug"])
            cmd.status = final_status
            cmd.finished_at = timezone.now()
            cmd.last_result = data.get("result", {})
            cmd.last_error_code = data.get("error_code", "")
            cmd.last_error_message = data.get("error_message", "")
            cmd.save(
                update_fields=[
                    "status",
                    "finished_at",
                    "last_result",
                    "last_error_code",
                    "last_error_message",
                ]
            )
