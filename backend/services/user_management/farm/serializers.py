from rest_framework import serializers
from .models import Farm, Barn, Zone


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = [
            "id",
            "name",
            "code",
            "location",
            "latitude",
            "longitude",
            "is_active",
            "created_at",
            "updated_at",
        ]


class BarnSerializer(serializers.ModelSerializer):
    farm = FarmSerializer(read_only=True)
    farm_id = serializers.PrimaryKeyRelatedField(
        queryset=Farm.objects.all(),
        source="farm",
        write_only=True,
    )

    class Meta:
        model = Barn
        fields = [
            "id",
            "name",
            "code",
            "description",
            "is_active",
            "farm",
            "farm_id",
            "created_at",
            "updated_at",
        ]


class ZoneSerializer(serializers.ModelSerializer):
    barn = BarnSerializer(read_only=True)
    barn_id = serializers.PrimaryKeyRelatedField(
        queryset=Barn.objects.all(),
        source="barn",
        write_only=True,
    )

    class Meta:
        model = Zone
        fields = [
            "id",
            "name",
            "code",
            "description",
            "is_active",
            "barn",
            "barn_id",
            "created_at",
            "updated_at",
        ]
