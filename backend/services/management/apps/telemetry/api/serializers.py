from rest_framework import serializers

class TelemetrySerializer(serializers.Serializer):
    device_id = serializers.CharField()
    livestock_id = serializers.CharField()
    metric = serializers.CharField()
    value = serializers.FloatField()
    recorded_at = serializers.DateTimeField(required=False)
