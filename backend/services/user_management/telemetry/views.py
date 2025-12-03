from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from api.permissions import IsAuthenticatedOrService
from .models import SensorReading
from .serializers import SensorReadingSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from devices.models import SensorType


class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.select_related("sensor", "sensor__device").all()
    serializer_class = SensorReadingSerializer
    permission_classes = [IsAuthenticatedOrService]

    def get_queryset(self):
        qs = super().get_queryset()
        sensor_id = self.request.query_params.get("sensor_id")
        if sensor_id:
            qs = qs.filter(sensor_id=sensor_id)
        return qs

class LatestReadingsView(APIView):
    """
    API برمی‌گرداند آخرین ریدینگ هر SensorType موردنیاز.
    اگر پارامتر query با نام ``sensor_types`` داده شود (CSV)، همان کدها بررسی می‌شوند،
    در غیر این صورت پیش‌فرض temperature و ammonia است.
    """

    permission_classes = [IsAuthenticatedOrService]

    def get(self, request, format=None):
        requested_types = request.query_params.get(
            "sensor_types", "temperature,ammonia"
        )
        type_codes = [code.strip() for code in requested_types.split(",") if code.strip()]

        sensor_types = SensorType.objects.filter(code__in=type_codes).values_list(
            "id", "code"
        )

        result = {code: None for code in type_codes}

        for sensor_type_id, code in sensor_types:
            latest_reading = (
                SensorReading.objects
                .select_related("sensor", "sensor__device", "sensor__sensor_type")
                .filter(sensor__sensor_type_id=sensor_type_id)
                .order_by("-ts")
                .first()
            )
            if latest_reading:
                result[code] = SensorReadingSerializer(latest_reading).data

        return Response(result)




