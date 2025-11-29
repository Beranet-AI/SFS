from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions
from .models import SensorReading
from .serializers import SensorReadingSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.select_related("sensor", "sensor__device").all()
    serializer_class = SensorReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        sensor_id = self.request.query_params.get("sensor_id")
        if sensor_id:
            qs = qs.filter(sensor_id=sensor_id)
        return qs

class LatestReadingsView(APIView):
    """
    API برمی‌گرداند آخرین ریدینگ دما (sensor_id=1)
    و آخرین ریدینگ آمونیاک (sensor_id=2).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        result = {}

        # آخرین ریدینگ دما (Sensor 1)
        temp_reading = (
            SensorReading.objects
            .filter(sensor_id=1)
            .order_by("-ts")
            .first()
        )
        if temp_reading:
            result["temperature"] = SensorReadingSerializer(temp_reading).data
        else:
            result["temperature"] = None

        # آخرین ریدینگ آمونیاک (Sensor 2)
        ammonia_reading = (
            SensorReading.objects
            .filter(sensor_id=2)
            .order_by("-ts")
            .first()
        )
        if ammonia_reading:
            result["ammonia"] = SensorReadingSerializer(ammonia_reading).data
        else:
            result["ammonia"] = None

        return Response(result)



