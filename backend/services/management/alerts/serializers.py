from rest_framework import serializers

from alerts.models import AlertLog, AlertRule
from devices.models import Sensor


class AlertRuleSerializer(serializers.ModelSerializer):
    sensor_id = serializers.PrimaryKeyRelatedField(
        source="sensor",
        queryset=Sensor.objects.all(),
        write_only=True,
    )

    class Meta:
        model = AlertRule
        fields = [
            "id",
            "sensor",
            "sensor_id",
            "threshold_value",
            "operator",
            "enabled",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["sensor", "created_at", "updated_at"]


class AlertLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertLog
        fields = [
            "id",
            "sensor",
            "value",
            "triggered_at",
            "alert_rule",
        ]
        read_only_fields = fields
