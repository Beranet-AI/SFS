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
    """
    Discovery list is NOT persisted in management.
    This endpoint is kept for compatibility.
    """
    return Response([])


@api_view(["POST"])
def upsert_discovery(request):
    """
    Discovery payload comes from edge.
    We validate it but do NOT store it.
    """
    ser = DeviceDiscoverySerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    return Response(
        ser.validated_data,
        status=status.HTTP_200_OK,
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
