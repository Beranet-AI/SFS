# File: livestock/api/serializers/disease_serializer.py
from rest_framework import serializers

class TreatmentSerializer(serializers.Serializer):
    disease_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    diagnosed_at = serializers.DateTimeField(required=False, allow_null=True)
    medication_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    milk_withdrawal_days = serializers.IntegerField(required=False, allow_null=True)
    treatment_completed = serializers.BooleanField(required=False, default=False)
