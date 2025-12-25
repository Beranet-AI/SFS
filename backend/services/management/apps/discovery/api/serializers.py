from rest_framework import serializers
from apps.discovery.models import DeviceDiscoveryModel
from apps.devices.models import DeviceModel
from django.utils import timezone

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

    def approve(self, discovery: DeviceDiscoveryModel) -> DeviceModel:
        data = self.validated_data
        device = DeviceModel.objects.create(
            name=data.get("name") or discovery.name,
            device_type=discovery.device_type,
            protocol=discovery.protocol,
            role=discovery.role,
            farm_id=data.get("farm_id") or None,
            barn_id=data.get("barn_id") or None,
            zone_id=data.get("zone_id") or None,
            livestock_id=data.get("livestock_id") or None,
            status=DeviceModel.Status.ACTIVE,
            last_seen=discovery.last_seen,
            meta=discovery.meta,
        )

        discovery.is_approved = True
        discovery.approved_at = timezone.now()
        discovery.save(update_fields=["is_approved", "approved_at"])
        return device
