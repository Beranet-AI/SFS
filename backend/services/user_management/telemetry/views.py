from rest_framework.views import APIView
from rest_framework.response import Response
from devices.models import SensorType
from telemetry.models import SensorReading
from telemetry.serializers import SensorReadingSerializer
from api.permissions import IsAuthenticatedOrService


class LatestReadingsView(APIView):
    """
    API برمی‌گرداند آخرین ریدینگ هر SensorType موردنیاز.
    اگر پارامتر query با نام ``sensor_types`` داده شود (CSV)، همان کدها بررسی می‌شوند،
    در غیر این صورت پیش‌فرض temperature و ammonia است.
    """

    permission_classes = [IsAuthenticatedOrService]

    def get(self, request, format=None):
        requested_types = request.query_params.get("sensor_types", "temperature,ammonia")
        type_codes = [code.strip().lower() for code in requested_types.split(",") if code.strip()]

        # دیکشنری با کلیدهای پایین‌حروفی
        result = {code: None for code in type_codes}

        # خواندن همه sensor types با درنظر گرفتن lowercase
        sensor_types = SensorType.objects.all()
        sensor_type_map = {s.code.lower(): s.id for s in sensor_types if s.code.lower() in type_codes}

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
