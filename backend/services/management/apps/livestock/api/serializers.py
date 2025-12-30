from rest_framework import serializers


class LivestockSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    tag = serializers.CharField()
    farm_id = serializers.CharField()
    barn = serializers.CharField()
    zone = serializers.CharField()
    health_state = serializers.CharField()
    health_confidence = serializers.FloatField()
    health_evaluated_at = serializers.DateTimeField()


class LivestockSensorGroupSerializer(serializers.Serializer):
    livestock_id = serializers.CharField()
    rfid_device_id = serializers.CharField()
    sensor_device_ids = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True,
        required=False,
    )
