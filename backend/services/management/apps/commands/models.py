import uuid
from django.db import models
from django.utils import timezone


class CommandStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    DISPATCHED = "dispatched", "Dispatched"
    ACKED = "acked", "Acked"
    RUNNING = "running", "Running"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED = "failed", "Failed"
    TIMED_OUT = "timed_out", "Timed out"
    CANCELLED = "cancelled", "Cancelled"
    DEAD_LETTERED = "dead_lettered", "Dead lettered"


class CommandTargetKind(models.TextChoices):
    DEVICE = "device", "Device"
    LIVESTOCK = "livestock", "Livestock"
    LOCATION = "location", "Location"


class CommandModel(models.Model):
    """
    Single source of truth for all commands:
    - manual control
    - rule-based automation
    - AI-driven decisions
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # semantic name of the command
    command_name = models.CharField(max_length=120)

    # target abstraction
    target_kind = models.CharField(
        max_length=20,
        choices=CommandTargetKind.choices,
        default=CommandTargetKind.DEVICE,
    )
    target_id = models.CharField(max_length=64, db_index=True)

    # execution routing
    edge_node_id = models.CharField(max_length=64, blank=True, default="")

    # execution payload
    payload = models.JSONField(default=dict, blank=True)

    # idempotency / deduplication
    idempotency_key = models.CharField(max_length=128, blank=True, default="")

    # lifecycle
    status = models.CharField(
        max_length=20,
        choices=CommandStatus.choices,
        default=CommandStatus.PENDING,
        db_index=True,
    )

    # audit
    source = models.CharField(max_length=16, default="manual")
    created_by = models.CharField(max_length=64, blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)

    # execution policy
    ack_deadline_sec = models.IntegerField(default=10)
    result_deadline_sec = models.IntegerField(default=60)
    max_attempts = models.IntegerField(default=5)

    # timing
    acked_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    # result / error
    last_error_code = models.CharField(max_length=64, blank=True, default="")
    last_error_message = models.TextField(blank=True, default="")
    last_result = models.JSONField(default=dict, blank=True)

    class Meta:
        app_label = "commands"
        db_table = "commands_command"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["target_kind", "target_id"]),
            models.Index(fields=["edge_node_id"]),
            models.Index(fields=["idempotency_key"]),
        ]

    # ---- lifecycle helpers ----

    def mark_dispatched(self):
        self.status = CommandStatus.DISPATCHED
        self.save(update_fields=["status"])

    def mark_acked(self, meta: dict | None = None):
        self.status = CommandStatus.ACKED
        self.acked_at = timezone.now()
        if meta:
            self.last_result = {**(self.last_result or {}), "ack": meta}
        self.save(update_fields=["status", "acked_at", "last_result"])

    def mark_running(self, meta: dict | None = None):
        self.status = CommandStatus.RUNNING
        self.started_at = timezone.now()
        if meta:
            self.last_result = {**(self.last_result or {}), "running": meta}
        self.save(update_fields=["status", "started_at", "last_result"])

    def mark_succeeded(self, result: dict | None = None):
        self.status = CommandStatus.SUCCEEDED
        self.finished_at = timezone.now()
        if result is not None:
            self.last_result = result
        self.save(update_fields=["status", "finished_at", "last_result"])

    def mark_failed(self, code: str = "", message: str = "", result: dict | None = None):
        self.status = CommandStatus.FAILED
        self.finished_at = timezone.now()
        self.last_error_code = code or ""
        self.last_error_message = message or ""
        if result is not None:
            self.last_result = result
        self.save(
            update_fields=[
                "status",
                "finished_at",
                "last_error_code",
                "last_error_message",
                "last_result",
            ]
        )


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
