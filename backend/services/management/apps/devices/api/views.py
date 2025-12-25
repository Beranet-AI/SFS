from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.devices.infrastructure.models.device_model import DeviceModel, DeviceStatus, ApprovalStatus
from apps.devices.infrastructure.models.device_discovery_model import DeviceDiscoveryModel, DiscoveryStatus

from .serializers import (
    DeviceSerializer,
    DeviceDiscoverySerializer,
    DeviceApproveSerializer,
)


@api_view(["GET"])
def list_devices(request):
    qs = DeviceModel.objects.all().order_by("-updated_at")
    return Response(DeviceSerializer(qs, many=True).data)


@api_view(["GET"])
def list_discoveries(request):
    status_q = request.query_params.get("status")
    qs = DeviceDiscoveryModel.objects.all().order_by("-updated_at")
    if status_q:
        qs = qs.filter(status=status_q)
    return Response(DeviceDiscoverySerializer(qs, many=True).data)


@api_view(["POST"])
def upsert_discovery(request):
    """
    Called by edge_controller:
    - Upsert by serial
    - Always refresh last_seen_at
    """
    payload = request.data or {}
    serial = payload.get("serial")
    if not serial:
        return Response({"detail": "serial is required"}, status=400)

    obj, created = DeviceDiscoveryModel.objects.get_or_create(
        serial=serial,
        defaults={
            "device_type": payload.get("device_type", "unknown"),
            "protocol": payload.get("protocol", "http_json"),
            "display_name": payload.get("display_name", ""),
            "metadata": payload.get("metadata", {}),
            "farm_id": payload.get("farm_id"),
            "barn_id": payload.get("barn_id"),
            "zone_id": payload.get("zone_id"),
            "livestock_id": payload.get("livestock_id"),
        },
    )

    # Update on every ping
    obj.device_type = payload.get("device_type", obj.device_type)
    obj.protocol = payload.get("protocol", obj.protocol)
    obj.display_name = payload.get("display_name", obj.display_name)
    obj.metadata = payload.get("metadata", obj.metadata) or {}
    obj.farm_id = payload.get("farm_id", obj.farm_id)
    obj.barn_id = payload.get("barn_id", obj.barn_id)
    obj.zone_id = payload.get("zone_id", obj.zone_id)
    obj.livestock_id = payload.get("livestock_id", obj.livestock_id)
    obj.last_seen_at = timezone.now()
    if obj.status != DiscoveryStatus.APPROVED:  # keep approved as approved
        obj.status = DiscoveryStatus.PENDING
    obj.save()

    return Response(DeviceDiscoverySerializer(obj).data, status=201 if created else 200)


@api_view(["POST"])
def approve_discovery(request):
    """
    Admin approves a discovered device and it becomes an active DeviceModel.
    """
    ser = DeviceApproveSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    data = ser.validated_data
    serial = data["serial"]

    try:
        discovery = DeviceDiscoveryModel.objects.get(serial=serial)
    except DeviceDiscoveryModel.DoesNotExist:
        return Response({"detail": "discovery not found"}, status=404)

    device, _ = DeviceModel.objects.get_or_create(
        serial=serial,
        defaults={
            "device_type": discovery.device_type,
            "protocol": discovery.protocol,
        },
    )

    # apply updates
    device.kind = data.get("kind", device.kind)
    device.display_name = data.get("display_name", device.display_name or discovery.display_name)

    device.farm_id = data.get("farm_id", discovery.farm_id)
    device.barn_id = data.get("barn_id", discovery.barn_id)
    device.zone_id = data.get("zone_id", discovery.zone_id)
    device.livestock_id = data.get("livestock_id", discovery.livestock_id)

    device.metadata = data.get("metadata", discovery.metadata) or {}
    device.capabilities = data.get("capabilities", device.capabilities) or {}

    device.status = DeviceStatus.ACTIVE
    device.approval_status = ApprovalStatus.APPROVED
    device.last_seen_at = discovery.last_seen_at
    device.save()

    discovery.status = DiscoveryStatus.APPROVED
    discovery.save(update_fields=["status", "updated_at"])

    return Response(DeviceSerializer(device).data, status=status.HTTP_200_OK)
