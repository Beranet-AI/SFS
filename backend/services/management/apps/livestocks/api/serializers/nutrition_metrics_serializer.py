# File: livestock/api/serializers/nutrition_metrics_serializer.py
from rest_framework import serializers

class NutritionMetricsSerializer(serializers.Serializer):
    feed_intake_kg = serializers.FloatField()
    water_intake_l = serializers.FloatField()
    feeder_station_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
