from rest_framework import serializers

from devices.models import Sensor, SensorType
from farm.models import Barn, Farm, Zone
from livestock.models import Animal

from .models import Alert, AlertRule


class AlertRuleSerializer(serializers.ModelSerializer):
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
        model = AlertRule
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


class AlertSerializer(serializers.ModelSerializer):
    farm_id = serializers.PrimaryKeyRelatedField(
        queryset=Farm.objects.all(),
        source="farm",
        write_only=True,
    )
    barn_id = serializers.PrimaryKeyRelatedField(
        queryset=Barn.objects.all(),
        source="barn",
        write_only=True,
        allow_null=True,
        required=False,
    )
    zone_id = serializers.PrimaryKeyRelatedField(
        queryset=Zone.objects.all(),
        source="zone",
        write_only=True,
        allow_null=True,
        required=False,
    )
    sensor_id = serializers.PrimaryKeyRelatedField(
        queryset=Sensor.objects.all(),
        source="sensor",
        write_only=True,
        allow_null=True,
        required=False,
    )
    animal_id = serializers.PrimaryKeyRelatedField(
        queryset=Animal.objects.all(),
        source="animal",
        write_only=True,
        allow_null=True,
        required=False,
    )
    rule_id = serializers.PrimaryKeyRelatedField(
        queryset=AlertRule.objects.all(),
        source="rule",
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Alert
        fields = [
            "id",
            "rule",
            "rule_id",
            "farm",
            "farm_id",
            "barn",
            "barn_id",
            "zone",
            "zone_id",
            "sensor",
            "sensor_id",
            "animal",
            "animal_id",
            "severity",
            "reading_value",
            "message",
            "status",
            "raised_at",
            "resolved_at",
            "extra_data",
            "created_at",
        ]
        read_only_fields = [
            "rule",
            "farm",
            "barn",
            "zone",
            "sensor",
            "animal",
            "created_at",
        ]
