from rest_framework import serializers
from .models import AlertRule, Alert
from farm.models import Farm, Barn, Zone
from devices.models import Sensor
from livestock.models import Animal


class AlertRuleSerializer(serializers.ModelSerializer):
    farm_id = serializers.PrimaryKeyRelatedField(
        queryset=Farm.objects.all(),
        source="farm",
        write_only=True,
    )

    class Meta:
        model = AlertRule
        fields = [
            "id",
            "name",
            "description",
            "farm",
            "farm_id",
            "scope",
            "severity",
            "condition_expression",
            "params",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["farm", "created_at", "updated_at"]
        

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
