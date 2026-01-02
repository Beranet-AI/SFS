# File: livestock/api/serializers/livestock_identity_serializer.py
from rest_framework import serializers

class LivestockIdentitySerializer(serializers.Serializer):
    livestock_id = serializers.CharField()
    tag_id = serializers.CharField()
    breed = serializers.CharField()
    birth_date = serializers.DateField(required=False, allow_null=True)
    sex = serializers.ChoiceField(choices=["MALE", "FEMALE"])
    herd_entry_date = serializers.DateField(required=False, allow_null=True)
    status = serializers.ChoiceField(choices=["ACTIVE", "INACTIVE", "CULLED", "DELETED"])
