import uuid
from django.db import models
from django.utils import timezone


class TelemetrySchemaModel(models.Model):
    """
    Registry of telemetry schemas.
    Defines how telemetry must look for a given device_type.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    device_type = models.CharField(
        max_length=64,
        db_index=True,
        help_text="Logical device type (e.g. ENVIRONMENTAL, LIVESTOCK)",
    )

    version = models.CharField(max_length=16, help_text="Schema version (e.g. v1)")

    json_schema = models.JSONField(help_text="Official JSON Schema definition")

    raw_example = models.JSONField(
        help_text="Example raw telemetry payload (for admin understanding)"
    )

    is_active = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    created_by = models.CharField(max_length=128, help_text="Who registered this schema")
    approved_by = models.CharField(
        max_length=128, null=True, blank=True, help_text="Who approved this schema"
    )

    class Meta:
        db_table = "telemetry_schemas"
        unique_together = ("device_type", "version")
        ordering = ["device_type", "-created_at"]
        indexes = [models.Index(fields=["device_type", "is_active"])]

    def approve(self, approved_by: str) -> None:
        self.is_active = True
        self.approved_by = approved_by
        self.approved_at = timezone.now()
        self.save(update_fields=["is_active", "approved_by", "approved_at"])

    @classmethod
    def next_version(cls, device_type: str) -> str:
        count = cls.objects.filter(device_type=device_type).count()
        return f"v{count + 1}"

    def __str__(self) -> str:
        return f"TelemetrySchema({self.device_type}, {self.version})"
