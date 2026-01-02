# File: livestock/api/serializers/ai_insight_serializer.py
from rest_framework import serializers

class LivestockAIInsightSerializer(serializers.Serializer):
    livestock_id = serializers.CharField()
    risk_score = serializers.FloatField(allow_null=True)
    health_score = serializers.FloatField(allow_null=True)
    ai = serializers.DictField(allow_null=True)
    appetite_change = serializers.CharField(allow_null=True)
    abnormal_milk_drop = serializers.BooleanField(allow_null=True)
    treatment_response = serializers.CharField(allow_null=True)
