from django.db import models

# Create your models here.

from django.db import models
from farm.models import Farm, Barn, Zone
from devices.models import Sensor
from livestock.models import Animal


class AlertRule(models.Model):
    SCOPE_CHOICES = (
        ("sensor", "Sensor"),
        ("barn", "Barn"),
        ("farm", "Farm"),
        ("animal", "Animal"),
    )

    SEVERITY_CHOICES = (
        ("info", "Info"),
        ("warn", "Warning"),
        ("critical", "Critical"),
    )

    name = models.CharField(
        max_length=200,
        help_text="نام قانون هشدار (مثلاً High Temperature in Barn 1)"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="توضیح قانون هشدار"
    )

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="alert_rules",
        help_text="این قانون برای کدام مزرعه است؟"
    )

    scope = models.CharField(
        max_length=20,
        choices=SCOPE_CHOICES,
        default="sensor",
        help_text="دامنه‌ی قانون (سنسور، سالن، مزرعه، دام)"
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default="warn",
    )

    # این فیلد یک expression یا شناسه‌ی قانون است؛
    # بعداً در سرویس AI/Rule Engine تفسیر می‌شود.
    condition_expression = models.CharField(
        max_length=500,
        help_text="عبارت شرطی (مثلاً temp > 30 برای 10 دقیقه)"
    )

    # در صورت نیاز، پارامترهای اضافی (آستانه‌ها، بازه‌ی زمانی، ...) را
    # می‌توان در این JSON نگه داشت
    params = models.JSONField(
        null=True,
        blank=True,
        help_text="پارامترهای قانون (thresholds, window, ...)"
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
        help_text="قانونی که این هشدار را ایجاد کرده (در صورت وجود)"
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

    message = models.TextField(
        help_text="پیام هشدار برای نمایش به کاربر"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
    )

    raised_at = models.DateTimeField(
        help_text="زمان ایجاد هشدار"
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="زمان برطرف شدن هشدار (در صورت وجود)"
    )

    extra_data = models.JSONField(
        null=True,
        blank=True,
        help_text="داده‌های کمکی (مقادیر سنسور، context، ...)"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "alerts"
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"
        indexes = [
            models.Index(fields=["farm", "severity", "status"]),
            models.Index(fields=["sensor", "raised_at"]),
        ]
        ordering = ["-raised_at"]

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.message[:40]}..."
