# File: livestock/api/serializers/reproduction_serializer.py
from rest_framework import serializers

class ReproductionSerializer(serializers.Serializer):
    estrus = serializers.BooleanField()
    pregnant = serializers.BooleanField()
    insemination_date = serializers.DateField(required=False, allow_null=True)
    insemination_method = serializers.ChoiceField(choices=["NATURAL", "AI"], required=False, allow_null=True)
    insemination_result = serializers.ChoiceField(choices=["PENDING", "SUCCESS", "FAILED"], required=False, allow_null=True)
    calving_date = serializers.DateField(required=False, allow_null=True)
