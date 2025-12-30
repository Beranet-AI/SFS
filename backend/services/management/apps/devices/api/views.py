from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    DeviceSerializer,
    DeviceDiscoverySerializer,
    DeviceApproveSerializer,
    RegisterEnvironmentalSensorSerializer,
    RegisterControlDeviceSerializer,
)
from apps.devices.application.services.device_service import DeviceService
from apps.devices.application.use_cases.register_control_device.use_case import (
    RegisterControlDeviceUseCase,
)
from apps.devices.application.use_cases.register_environmental_sensor.use_case import (
    RegisterEnvironmentalSensorUseCase,
)
from apps.devices.mappers.control_device_mapper import ControlDeviceMapper
from apps.devices.mappers.environmental_sensor_mapper import (
    EnvironmentalSensorMapper,
)


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


@api_view(["POST"])
def register_environmental_sensor(request):
    ser = RegisterEnvironmentalSensorSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    input_dto = EnvironmentalSensorMapper.from_payload(ser.validated_data)
    result = RegisterEnvironmentalSensorUseCase().execute(input_dto)

    return Response(
        EnvironmentalSensorMapper.to_response(result),
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def register_control_device(request):
    ser = RegisterControlDeviceSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    input_dto = ControlDeviceMapper.from_payload(ser.validated_data)
    result = RegisterControlDeviceUseCase().execute(input_dto)

    return Response(
        ControlDeviceMapper.to_response(result),
        status=status.HTTP_201_CREATED,
    )
