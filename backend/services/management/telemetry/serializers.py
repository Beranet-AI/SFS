from typing import Any, Dict

from django.utils import timezone
from rest_framework import serializers

from alerts.services import evaluate_alerts_for_reading
from devices.models import Sensor
from telemetry.models import SensorReading

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
