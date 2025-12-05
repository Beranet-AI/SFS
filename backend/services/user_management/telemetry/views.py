from typing import Any, Dict, List, Optional
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from devices.models import SensorType
from telemetry.models import SensorReading
from telemetry.serializers import SensorReadingSerializer
from api.permissions import IsAuthenticatedOrService

class LatestReadingsView(APIView):
    """
    API برمی‌گرداند آخرین ریدینگ هر SensorType موردنیاز.
    اگر پارامتر query با نام ``sensor_types`` داده شود (CSV)، همان کدها بررسی می‌شوند،
    در غیر این صورت از تمام SensorType‌های موجود استفاده می‌شود.
    """
    permission_classes = [IsAuthenticatedOrService]

    def get(self, request: Request, format: Optional[str] = None) -> Response:
        requested_types = request.query_params.get("sensor_types")
        sensor_types_qs = SensorType.objects.all()

        if requested_types:
            # اگر پارامتر داده شده باشد، فقط کدهای معتبر (موجود در دیتابیس) را در نظر می‌گیریم
            raw_codes: List[str] = [code.strip() for code in requested_types.split(",") if code.strip()]
            sensor_type_map: Dict[str, int] = {
                s.code.lower(): s.id for s in sensor_types_qs if s.code.lower() in raw_codes
            }
            type_codes: List[str] = [code for code in raw_codes if code in sensor_type_map]
        else:
            # در غیر این صورت، تمام SensorType‌های موجود استفاده می‌شوند
            sensor_type_map: Dict[str, int] = {s.code.lower(): s.id for s in sensor_types_qs}
            type_codes: List[str] = list(sensor_type_map.keys())

        result: Dict[str, Any] = {code: None for code in type_codes}

        for code in type_codes:
            sensor_type_id = sensor_type_map.get(code)
            if not sensor_type_id:
                continue
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
