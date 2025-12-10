from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAuthenticatedOrService
from .models import SensorReading
from .serializers import SensorReadingSerializer
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
    API آخرین ریدینگ برای هر SensorType را برمی‌گرداند.
    """

    permission_classes = [IsAuthenticatedOrService]

    def get(self, request, format=None):
        requested_types = request.query_params.get("sensor_types", "temperature,ammonia")
        type_codes = [code.strip() for code in requested_types.split(",") if code.strip()]

        sensor_types = SensorType.objects.filter(code__in=type_codes).values_list("id", "code")
        result = {code: None for code in type_codes}

        for sensor_type_id, code in sensor_types:
            latest_reading = (
                SensorReading.objects.select_related("sensor", "sensor__device", "sensor__sensor_type")
                .filter(sensor__sensor_type_id=sensor_type_id)
                .order_by("-ts")
                .first()
            )
            if latest_reading:
                result[code] = SensorReadingSerializer(latest_reading).data

        return Response(result)


class HistoricalReadingsView(APIView):
    """
    API برای بازگرداندن داده‌های تاریخی یک سنسور خاص.
    پارامترها:
      - sensor_id (الزامی)
      - limit (پیش‌فرض: 50)
      - ts__gte / ts__lte (اختیاری: فیلتر بر اساس بازه زمانی)
    """

    permission_classes = [IsAuthenticatedOrService]

    def get(self, request, format=None):
        sensor_id = request.query_params.get("sensor_id")
        if not sensor_id:
            return Response({"detail": "پارامتر sensor_id الزامی است."}, status=400)

        limit = int(request.query_params.get("limit", 50))
        ts_gte = request.query_params.get("ts__gte")
        ts_lte = request.query_params.get("ts__lte")

        qs = SensorReading.objects.filter(sensor_id=sensor_id)

        if ts_gte:
            qs = qs.filter(ts__gte=ts_gte)
        if ts_lte:
            qs = qs.filter(ts__lte=ts_lte)

        qs = qs.order_by("-ts")[:limit]

        serialized = SensorReadingSerializer(qs, many=True)
        return Response(serialized.data)
