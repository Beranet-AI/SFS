from django.core.exceptions import ValidationError
from django.db import models

from devices.models import Sensor, SensorType
from farm.models import Barn, Farm, Zone
from livestock.models import Animal


class AlertRule(models.Model):
    """Threshold-based alert rule for a sensor or sensor type."""

    OPERATOR_CHOICES = (
        ("greater_than", "Greater than"),
        ("less_than", "Less than"),
    )

    SEVERITY_CHOICES = (
        ("info", "Info"),
        ("warn", "Warning"),
        ("critical", "Critical"),
    )

    name = models.CharField(
        max_length=200,
        help_text="نام قانون هشدار (مثلاً High Temperature in Barn 1)",
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="توضیح قانون هشدار",
    )

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="alert_rules",
        help_text="این قانون برای کدام مزرعه است؟",
    )

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="alert_rules",
        null=True,
        blank=True,
        help_text="قانون برای یک سنسور مشخص",
    )

    sensor_type = models.ForeignKey(
        SensorType,
        on_delete=models.CASCADE,
        related_name="alert_rules",
        null=True,
        blank=True,
        help_text="یا بر اساس نوع سنسور اعمال شود",
    )

    threshold_value = models.FloatField(help_text="آستانهٔ هشدار")

    operator = models.CharField(
        max_length=20,
        choices=OPERATOR_CHOICES,
        default="greater_than",
        help_text="اپراتور مقایسه با آستانه",
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default="warn",
    )

    condition_expression = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text="عبارت شرطی اختیاری برای قوانین پیشرفته",
    )

    params = models.JSONField(
        null=True,
        blank=True,
        help_text="پارامترهای قانون (thresholds, window, ...)",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "alert_rules"
        verbose_name = "Alert Rule"
        verbose_name_plural = "Alert Rules"
        ordering = ["farm", "severity", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.farm.name})"

    def clean(self):
        if not (self.sensor or self.sensor_type):
            raise ValidationError("حداقل یکی از سنسور یا نوع سنسور باید مشخص شود.")

    def save(self, *args, **kwargs):
        # If a sensor is provided, derive farm automatically for consistency
        if self.sensor and not self.farm_id:
            device = getattr(self.sensor, "device", None)
            if device and device.farm_id:
                self.farm_id = device.farm_id
        super().save(*args, **kwargs)


class Alert(models.Model):
    STATUS_CHOICES = (
        ("open", "Open"),
        ("ack", "Acknowledged"),
        ("resolved", "Resolved"),
    )

    SEVERITY_CHOICES = (
        ("info", "Info"),
        ("warn", "Warning"),
        ("critical", "Critical"),
    )

    rule = models.ForeignKey(
        AlertRule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alerts",
        help_text="قانونی که این هشدار را ایجاد کرده (در صورت وجود)",
    )

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="alerts",
    )
    barn = models.ForeignKey(
        Barn,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alerts",
    )
    zone = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alerts",
    )

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alerts",
    )
    animal = models.ForeignKey(
        Animal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alerts",
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default="warn",
    )

    reading_value = models.FloatField(
        null=True,
        blank=True,
        help_text="مقدار خوانده‌شده که قانون را نقض کرده است",
    )

    message = models.TextField(
        help_text="پیام هشدار برای نمایش به کاربر",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
    )

    raised_at = models.DateTimeField(
        help_text="زمان ایجاد هشدار",
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="زمان برطرف شدن هشدار (در صورت وجود)",
    )

    extra_data = models.JSONField(
        null=True,
        blank=True,
        help_text="داده‌های کمکی (مقادیر سنسور، context، ...)",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "alerts"
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"
        indexes = [
            models.Index(fields=["farm", "severity", "status"]),
            models.Index(fields=["sensor", "raised_at"]),
            models.Index(fields=["status", "raised_at"]),
        ]
        ordering = ["-raised_at"]

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.message[:40]}..."
