from rest_framework import serializers
from .models import Animal, RfidTag
from farm.models import Farm, Barn, Zone


class RfidTagSerializer(serializers.ModelSerializer):
    farm_id = serializers.PrimaryKeyRelatedField(
        queryset=Farm.objects.all(),
        source="farm",
        write_only=True,
    )

    class Meta:
        model = RfidTag
        fields = [
            "id",
            "tag_code",
            "status",
            "description",
            "farm",
            "farm_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["farm", "created_at", "updated_at"]


class AnimalSerializer(serializers.ModelSerializer):
    farm_id = serializers.PrimaryKeyRelatedField(
        queryset=Farm.objects.all(),
        source="farm",
        write_only=True,
    )
    barn_id = serializers.PrimaryKeyRelatedField(
        queryset=Barn.objects.all(),
        source="barn",
        write_only=True,
        allow_null=True,
        required=False,
    )
    current_zone_id = serializers.PrimaryKeyRelatedField(
        queryset=Zone.objects.all(),
        source="current_zone",
        write_only=True,
        allow_null=True,
        required=False,
    )
    rfid_tag_id = serializers.PrimaryKeyRelatedField(
        queryset=RfidTag.objects.all(),
        source="rfid_tag",
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Animal
        fields = [
            "id",
            "species",
            "breed",
            "external_id",
            "birth_date",
            "status",
            "notes",
            "farm",
            "barn",
            "current_zone",
            "rfid_tag",
            "farm_id",
            "barn_id",
            "current_zone_id",
            "rfid_tag_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "farm",
            "barn",
            "current_zone",
            "rfid_tag",
            "created_at",
            "updated_at",
        ]

