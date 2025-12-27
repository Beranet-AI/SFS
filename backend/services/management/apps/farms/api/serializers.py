from rest_framework import serializers
from apps.farms.models import FarmModel


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmModel
        fields = ("id", "name", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
