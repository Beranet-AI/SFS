# farm/api/serializers/environment_metrics_serializer.py
from rest_framework import serializers

class EnvironmentMetricsSerializer(serializers.Serializer):
    temperature_c = serializers.FloatField()
    humidity = serializers.FloatField()
    ammonia_ppm = serializers.FloatField()
    co2_ppm = serializers.FloatField(required=False, allow_null=True)
    airflow_mps = serializers.FloatField(required=False, allow_null=True)
