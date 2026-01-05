import uuid

from django.db import models
from django.utils import timezone

from .command_model import CommandModel


class CommandAttemptModel(models.Model):
    """
    Each delivery attempt (retry + audit).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    command = models.ForeignKey(
        CommandModel,
        on_delete=models.CASCADE,
        related_name="attempts",
    )

    attempt_no = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    dispatched_at = models.DateTimeField(null=True, blank=True)
    acked_at = models.DateTimeField(null=True, blank=True)
    result_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=32, default="created")

    executor_receipt = models.CharField(max_length=128, blank=True, default="")
    debug = models.JSONField(default=dict, blank=True)

    class Meta:
        app_label = "commands"
        db_table = "commands_attempt"
        unique_together = [("command", "attempt_no")]
        indexes = [
            models.Index(fields=["command", "attempt_no"]),
            models.Index(fields=["status", "created_at"]),
        ]


CommandExecutionModel = CommandAttemptModel
