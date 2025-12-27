from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.discovery.api.serializers import (
    DeviceDiscoverySerializer,
    ApproveDiscoverySerializer,
)
from apps.discovery.application.services.discovery_service import DiscoveryService


@api_view(["POST"])
def upsert_discovery(request):
    service = DiscoveryService()
    try:
        obj = service.upsert_discovery(data=request.data or {})
    except ValueError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(DeviceDiscoverySerializer(obj).data)


@api_view(["GET"])
def list_pending(request):
    service = DiscoveryService()
    qs = service.list_pending()
    return Response(DeviceDiscoverySerializer(qs, many=True).data)


@api_view(["POST"])
def approve(request, external_id: str):
    service = DiscoveryService()

    try:
        discovery = service.get_by_external_id(external_id=external_id)
    except Exception:
        return Response({"error": "not found"}, status=404)

    ser = ApproveDiscoverySerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    device = service.approve(
        discovery=discovery,
        data=ser.validated_data,
    )

    return Response({"ok": True, "device_id": device.id})
