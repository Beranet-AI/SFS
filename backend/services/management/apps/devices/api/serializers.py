from rest_framework import serializers
from apps.devices.models import DeviceModel


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceModel
        fields = "__all__"


class DeviceDiscoverySerializer(serializers.Serializer):
    """
    Discovery payload coming from edge.
    This is NOT a Django model.
    """

    serial = serializers.CharField()
    kind = serializers.CharField(required=False)
    display_name = serializers.CharField(required=False, allow_blank=True)

    farm_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    barn_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    zone_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    livestock_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    capabilities = serializers.JSONField(required=False)
    metadata = serializers.JSONField(required=False)
    status = serializers.CharField(required=False)


class DeviceApproveSerializer(serializers.Serializer):
    """
    Approve discovery and create/update DeviceModel
    """

    serial = serializers.CharField()
    kind = serializers.ChoiceField(
        choices=["sensor", "actuator", "gateway"],
        required=False,
    )
    display_name = serializers.CharField(required=False, allow_blank=True)

    farm_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    barn_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    zone_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    livestock_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    capabilities = serializers.JSONField(required=False)
    metadata = serializers.JSONField(required=False)
