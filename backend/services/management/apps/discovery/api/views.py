from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.discovery.models import DeviceDiscoveryModel
from apps.discovery.api.serializers import DeviceDiscoverySerializer, ApproveDiscoverySerializer

@api_view(["POST"])
def upsert_discovery(request):
    """
    data_ingestion -> management
    """
    ext_id = request.data.get("external_id")
    if not ext_id:
        return Response({"error": "external_id required"}, status=status.HTTP_400_BAD_REQUEST)

    obj, _ = DeviceDiscoveryModel.objects.update_or_create(
        external_id=ext_id,
        defaults={
            "name": request.data.get("name", "unknown"),
            "device_type": request.data.get("device_type", "unknown"),
            "protocol": request.data.get("protocol", "unknown"),
            "role": request.data.get("role", "sensor"),
            "ip": request.data.get("ip"),
            "meta": request.data.get("meta") or {},
            "last_seen": request.data.get("last_seen"),
        },
    )
    return Response(DeviceDiscoverySerializer(obj).data)

@api_view(["GET"])
def list_pending(request):
    qs = DeviceDiscoveryModel.objects.filter(is_approved=False).order_by("-created_at")
    return Response(DeviceDiscoverySerializer(qs, many=True).data)

@api_view(["POST"])
def approve(request, external_id: str):
    try:
        d = DeviceDiscoveryModel.objects.get(external_id=external_id)
    except DeviceDiscoveryModel.DoesNotExist:
        return Response({"error": "not found"}, status=404)

    ser = ApproveDiscoverySerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    device = ser.approve(d)
    return Response({"ok": True, "device_id": device.id})
