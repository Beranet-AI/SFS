from django.core.exceptions import ValidationError
from django.db import models

from devices.models import Sensor, SensorType
from farm.models import Barn, Farm, Zone
from livestock.models import Animal


class LiveStatusRule(models.Model):
    """Threshold-based rule for deriving live status from telemetry."""

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
        help_text="نام قانون وضعیت (مثلاً High Temperature in Barn 1)",
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="توضیح قانون وضعیت",
    )

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="live_status_rules",
        help_text="این قانون برای کدام مزرعه است؟",
    )

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="live_status_rules",
        null=True,
        blank=True,
        help_text="قانون برای یک سنسور مشخص",
    )

    sensor_type = models.ForeignKey(
        SensorType,
        on_delete=models.CASCADE,
        related_name="live_status_rules",
        null=True,
        blank=True,
        help_text="یا بر اساس نوع سنسور اعمال شود",
    )

    threshold_value = models.FloatField(help_text="آستانهٔ وضعیت")

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
        db_table = "live_status_rules"
        verbose_name = "Live Status Rule"
        verbose_name_plural = "Live Status Rules"
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


class LiveStatus(models.Model):
    STATE_CHOICES = (
        ("active", "Active"),
        ("cleared", "Cleared"),
    )

    SEVERITY_CHOICES = (
        ("info", "Info"),
        ("warn", "Warning"),
        ("critical", "Critical"),
    )

    rule = models.ForeignKey(
        LiveStatusRule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="live_statuses",
        help_text="قانونی که این وضعیت را ایجاد کرده (در صورت وجود)",
    )

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="live_statuses",
    )
    barn = models.ForeignKey(
        Barn,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="live_statuses",
    )
    zone = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="live_statuses",
    )

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="live_statuses",
    )
    animal = models.ForeignKey(
        Animal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="live_statuses",
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
        help_text="پیام وضعیت برای نمایش به کاربر",
    )

    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default="active",
    )

    raised_at = models.DateTimeField(
        help_text="زمان ایجاد وضعیت",
    )
    cleared_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="زمان برطرف شدن وضعیت (در صورت وجود)",
    )

    extra_data = models.JSONField(
        null=True,
        blank=True,
        help_text="داده‌های کمکی (مقادیر سنسور، context، ...)",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "live_statuses"
        verbose_name = "Live Status"
        verbose_name_plural = "Live Statuses"
        indexes = [
            models.Index(fields=["farm", "severity", "state"]),
            models.Index(fields=["sensor", "raised_at"]),
            models.Index(fields=["state", "raised_at"]),
        ]
        ordering = ["-raised_at"]

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.message[:40]}..."
