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
