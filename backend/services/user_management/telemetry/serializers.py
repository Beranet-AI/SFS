import importlib
from typing import Any, Callable, Dict

from django.utils import timezone
from rest_framework import serializers

from devices.models import Sensor
from telemetry.models import SensorReading


AlertEvaluator = Callable[[SensorReading], None]


def _resolve_alert_evaluator() -> AlertEvaluator:
    """Return the alert evaluation hook if the alerting service is installed.

    The user_management service may run without the alerting package in its
    image, so we lazily import the evaluator only when the module exists.
    """
    try:
        spec = importlib.util.find_spec("alerting.alerts.services")
    except ModuleNotFoundError:
        return lambda reading: None

    if spec is None:
        return lambda reading: None

    module = importlib.import_module("alerting.alerts.services")
    return getattr(module, "evaluate_alerts_for_reading", lambda reading: None)


evaluate_alerts_for_reading: AlertEvaluator = _resolve_alert_evaluator()

class SensorReadingSerializer(serializers.ModelSerializer):
    # sensor_id را به فیلد FK مدل sensor نگاشت می‌کنیم
    sensor_id = serializers.PrimaryKeyRelatedField(
        source="sensor",              # توی مدل، فیلد sensor پر می‌شود
        queryset=Sensor.objects.all(),
        write_only=True
    )

    # مهم: ts دیگر required نیست
    ts = serializers.DateTimeField(required=False)

    class Meta:
        model = SensorReading
        fields = [
            "id",
            "sensor",      # فقط برای خروجی (read-only)
            "sensor_id",   # فقط برای ورودی (write-only)
            "ts",
            "value",
            "raw_payload",
            "quality",
            "created_at",
        ]
        read_only_fields = ["sensor", "created_at"]

    def create(self, validated_data: Dict[str, Any]) -> SensorReading:
        # اگر ts در Request نبود، الان (زمان حال) را قرار می‌دهیم
        if "ts" not in validated_data:
            validated_data["ts"] = timezone.now()
        reading = super().create(validated_data)
        evaluate_alerts_for_reading(reading)
        return reading
