import uuid

from django.db import models


class CommandAliasModel(models.Model):
    """
    CommandAliasModel

    This model defines a translation (alias) from a logical command
    (device_category, device_type, command_category, command_type)
    to a physical executable command name.

    IMPORTANT:
    - This table is ONLY for non-edge devices.
    - edge_controller commands must NEVER be resolved via this table.
    - execution_target is intentionally NOT stored here.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # Logical command identity (input side)
    device_category = models.CharField(
        max_length=64,
        help_text="Logical device category (e.g. Infrastructure, Sensor, Actuator)",
    )

    device_type = models.CharField(
        max_length=64,
        help_text="Logical device type (e.g. plc, temperature_sensor)",
    )

    command_category = models.CharField(
        max_length=64,
        help_text="Logical command category (e.g. Network, Control, Telemetry)",
    )

    command_type = models.CharField(
        max_length=64,
        help_text="Logical command type (e.g. Scan, Read, OnOff)",
    )

    # Physical command identity (output side)
    resolved_command_name = models.CharField(
        max_length=128,
        help_text="Executable command name understood by the target device",
    )

    # Control flag
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this command alias is active and selectable",
    )

    # Audit fields
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "command_aliases"
        verbose_name = "Command Alias"
        verbose_name_plural = "Command Aliases"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "device_category",
                    "device_type",
                    "command_category",
                    "command_type",
                ],
                name="uq_command_alias_unique_mapping",
            )
        ]

    def __str__(self) -> str:
        return (
            f"{self.device_category}/"
            f"{self.device_type} | "
            f"{self.command_category}/"
            f"{self.command_type} → "
            f"{self.resolved_command_name}"
        )
