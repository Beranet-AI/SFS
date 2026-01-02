# File: livestock/api/serializers/health_metrics_serializer.py
from rest_framework import serializers

class HealthMetricsSerializer(serializers.Serializer):
    temperature_c = serializers.FloatField()
    activity = serializers.FloatField()
    rumination_minutes = serializers.FloatField(required=False, allow_null=True)
    movement_index = serializers.FloatField(required=False, allow_null=True)
    lying_minutes = serializers.FloatField(required=False, allow_null=True)
    standing_minutes = serializers.FloatField(required=False, allow_null=True)
    heart_rate_bpm = serializers.IntegerField(required=False, allow_null=True)
