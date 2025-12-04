from django.shortcuts import render
from api.permissions import IsAuthenticatedOrService
# Create your views here.

from rest_framework import viewsets, permissions
from .models import Device, SensorType, Sensor
from .serializers import DeviceSerializer, SensorTypeSerializer, SensorSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.select_related("farm", "barn", "zone").all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsAuthenticatedOrService]


class SensorTypeViewSet(viewsets.ModelViewSet):
    queryset = SensorType.objects.all()
    serializer_class = SensorTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsAuthenticatedOrService]


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.select_related("device", "sensor_type").all()
    serializer_class = SensorSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsAuthenticatedOrService]
