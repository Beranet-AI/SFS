from rest_framework import serializers
from .models import Device, SensorType, Sensor
from farm.models import Farm, Barn, Zone


class DeviceSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Device
        fields = [
            "id",
            "name",
            "type",
            "serial_number",
            "ip_address",
            "status",
            "last_seen_at",
            "is_active",
            "farm",     # read-only detail
            "barn",     # read-only detail
            "zone",     # read-only detail
            "farm_id",  # write-only IDs
            "barn_id",
            "zone_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["farm", "barn", "zone", "created_at", "updated_at"]


class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = [
            "id",
            "code",
            "name",
            "unit",
            "min_value",
            "max_value",
        ]


class SensorSerializer(serializers.ModelSerializer):
    device_id = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all(),
        source="device",
        write_only=True,
    )
    sensor_type_id = serializers.PrimaryKeyRelatedField(
        queryset=SensorType.objects.all(),
        source="sensor_type",
        write_only=True,
    )

    class Meta:
        model = Sensor
        fields = [
            "id",
            "name",
            "hardware_address",
            "is_active",
            "device",
            "sensor_type",
            "device_id",
            "sensor_type_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["device", "sensor_type", "created_at", "updated_at"]
