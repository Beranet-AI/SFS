from django.db import models

from devices.models import Sensor


class AlertRule(models.Model):
    OPERATORS = (
        (">", ">"),
        ("<", "<"),
        (">=", ">="),
        ("<=", "<="),
        ("==", "=="),
        ("!=", "!="),
    )

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="alert_rules",
    )
    threshold_value = models.FloatField()
    operator = models.CharField(max_length=2, choices=OPERATORS)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "alert_rules"
        verbose_name = "Alert Rule"
        verbose_name_plural = "Alert Rules"
        indexes = [
            models.Index(fields=["sensor", "enabled"]),
        ]

    def __str__(self) -> str:
        return f"Rule {self.id} on {self.sensor} {self.operator} {self.threshold_value}"


class AlertLog(models.Model):
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="alert_logs",
    )
    value = models.FloatField()
    triggered_at = models.DateTimeField()
    alert_rule = models.ForeignKey(
        AlertRule,
        on_delete=models.CASCADE,
        related_name="logs",
    )

    class Meta:
        db_table = "alert_logs"
        verbose_name = "Alert Log"
        verbose_name_plural = "Alert Logs"
        indexes = [
            models.Index(fields=["sensor", "triggered_at"]),
            models.Index(fields=["alert_rule", "triggered_at"]),
        ]
        ordering = ["-triggered_at"]

    def __str__(self) -> str:
        return f"Alert on {self.sensor} at {self.triggered_at}: {self.value}"
