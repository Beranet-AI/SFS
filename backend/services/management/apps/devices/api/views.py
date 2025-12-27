from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    DeviceSerializer,
    DeviceDiscoverySerializer,
    DeviceApproveSerializer,
)
from apps.devices.application.services.device_service import DeviceService


@api_view(["GET"])
def list_devices(request):
    service = DeviceService()
    qs = service.list_devices()
    return Response(DeviceSerializer(qs, many=True).data)


@api_view(["GET"])
def list_discoveries(request):
    status_q = request.query_params.get("status")
    service = DeviceService()
    qs = service.list_discoveries(status=status_q)
    return Response(DeviceDiscoverySerializer(qs, many=True).data)


@api_view(["POST"])
def upsert_discovery(request):
    service = DeviceService()

    try:
        obj, created = service.upsert_discovery(payload=request.data or {})
    except ValueError as exc:
        return Response({"detail": str(exc)}, status=400)

    return Response(
        DeviceDiscoverySerializer(obj).data,
        status=201 if created else 200,
    )


@api_view(["POST"])
def approve_discovery(request):
    ser = DeviceApproveSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    service = DeviceService()
    device = service.approve_discovery(data=ser.validated_data)

    return Response(
        DeviceSerializer(device).data,
        status=status.HTTP_200_OK,
    )
