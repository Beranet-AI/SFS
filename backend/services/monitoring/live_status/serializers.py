from rest_framework import serializers

from devices.models import Sensor, SensorType
from farm.models import Barn, Farm, Zone
from livestock.models import Animal

from .models import LiveStatus, LiveStatusRule


class LiveStatusRuleSerializer(serializers.ModelSerializer):
    farm_id = serializers.PrimaryKeyRelatedField(
        queryset=Farm.objects.all(),
        source="farm",
        write_only=True,
    )
    sensor_id = serializers.PrimaryKeyRelatedField(
        queryset=Sensor.objects.all(),
        source="sensor",
        write_only=True,
        required=False,
        allow_null=True,
    )
    sensor_type_id = serializers.PrimaryKeyRelatedField(
        queryset=SensorType.objects.all(),
        source="sensor_type",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = LiveStatusRule
        fields = [
            "id",
            "name",
            "description",
            "farm",
            "farm_id",
            "sensor",
            "sensor_id",
            "sensor_type",
            "sensor_type_id",
            "threshold_value",
            "operator",
            "severity",
            "condition_expression",
            "params",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["farm", "created_at", "updated_at", "sensor", "sensor_type"]

    def validate(self, attrs):
        sensor = attrs.get("sensor") or getattr(self.instance, "sensor", None)
        sensor_type = attrs.get("sensor_type") or getattr(self.instance, "sensor_type", None)
        if not (sensor or sensor_type):
            raise serializers.ValidationError("حداقل یکی از سنسور یا نوع سنسور باید تنظیم شود.")
        return attrs


class LiveStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveStatus
        fields = [
            "id",
            "rule",
            "farm",
            "barn",
            "zone",
            "sensor",
            "animal",
            "severity",
            "reading_value",
            "message",
            "state",
            "raised_at",
            "cleared_at",
            "extra_data",
            "created_at",
        ]
        read_only_fields = fields
