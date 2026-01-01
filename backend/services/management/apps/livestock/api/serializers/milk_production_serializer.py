# File: livestock/api/serializers/milk_production_serializer.py
from rest_framework import serializers

class MilkProductionSerializer(serializers.Serializer):
    volume_l = serializers.FloatField()
    ec = serializers.FloatField()
    milk_temp_c = serializers.FloatField(required=False, allow_null=True)
    scc = serializers.IntegerField(required=False, allow_null=True)
