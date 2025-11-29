from rest_framework import serializers
from devices.models import Sensor
from telemetry.models import SensorReading
from django.utils import timezone


class SensorReadingSerializer(serializers.ModelSerializer):
    # sensor_id را به فیلد FK مدل sensor نگاشت می‌کنیم
    sensor_id = serializers.PrimaryKeyRelatedField(
        source="sensor",              # توی model فیلد sensor پر می‌شود
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

    def create(self, validated_data):
        # اگر ts در Request نبود، الان را بگذار
        if "ts" not in validated_data:
            validated_data["ts"] = timezone.now()
        return super().create(validated_data)


#نکات مهم:

#خط ts = serializers.DateTimeField(required=False) باعث می‌شه DRF دیگه نگه «ts اجباریه».

#در create اگر ts نیومده بود، خودمون timezone.now() می‌ذاریم.

#این کار بدون هیچ migration انجام می‌شه، فقط در لایه Serializer.



