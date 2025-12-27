from rest_framework import serializers

from apps.discovery.models import DeviceDiscoveryModel


class DeviceDiscoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceDiscoveryModel
        fields = "__all__"


class ApproveDiscoverySerializer(serializers.Serializer):
    # mapping
    farm_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    barn_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    zone_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    livestock_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    # copy overrides
    name = serializers.CharField(required=False)
    status = serializers.CharField(required=False, default="active")
