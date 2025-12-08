from collections import defaultdict

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthenticatedOrService
from devices.models import Sensor
from .models import Barn, Farm, Zone
from .serializers import BarnSerializer, FarmSerializer, ZoneSerializer


class IsActiveDefaultQuerysetMixin:
    """
    میکسین برای اینکه به‌صورت پیش‌فرض فقط رکوردهای is_active=True برگردند،
    مگر اینکه خلافش را خودت مشخص کنی.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)


class FarmViewSet(IsActiveDefaultQuerysetMixin, viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = [IsAuthenticatedOrService]


class BarnViewSet(IsActiveDefaultQuerysetMixin, viewsets.ModelViewSet):
    queryset = Barn.objects.select_related("farm").all()
    serializer_class = BarnSerializer
    permission_classes = [IsAuthenticatedOrService]


class ZoneViewSet(IsActiveDefaultQuerysetMixin, viewsets.ModelViewSet):
    queryset = Zone.objects.select_related("barn", "barn__farm").all()
    serializer_class = ZoneSerializer
    permission_classes = [IsAuthenticatedOrService]


class FarmHierarchyView(APIView):
    """بازگرداندن ساختار مزرعه ← بارن ← زون به همراه سنسورها"""

    permission_classes = [IsAuthenticatedOrService]

    def get(self, request):  # noqa: ANN001
        farms_qs = Farm.objects.filter(is_active=True).order_by("name")
        barns_qs = Barn.objects.filter(is_active=True).select_related("farm").order_by("name")
        zones_qs = Zone.objects.filter(is_active=True).select_related("barn", "barn__farm").order_by("name")

        sensors_qs = (
            Sensor.objects.select_related("device__farm", "device__barn", "device__zone", "sensor_type")
            .filter(
                is_active=True,
                device__is_active=True,
                device__farm__is_active=True,
            )
        )

        barns_by_farm = defaultdict(list)
        for barn in barns_qs:
            barns_by_farm[barn.farm_id].append(barn)

        zones_by_barn = defaultdict(list)
        for zone in zones_qs:
            zones_by_barn[zone.barn_id].append(zone)

        sensors_by_farm = defaultdict(list)
        sensors_by_barn = defaultdict(list)
        sensors_by_zone = defaultdict(list)

        for sensor in sensors_qs:
            device = sensor.device
            if not device:
                continue

            payload = {
                "id": sensor.id,
                "name": sensor.name,
                "device_id": device.id,
                "farm_id": device.farm_id,
                "barn_id": device.barn_id,
                "zone_id": device.zone_id,
                "sensor_type": {
                    "id": sensor.sensor_type_id,
                    "code": sensor.sensor_type.code,
                    "name": sensor.sensor_type.name,
                    "unit": sensor.sensor_type.unit,
                },
            }

            if device.zone_id:
                sensors_by_zone[device.zone_id].append(payload)
            elif device.barn_id:
                sensors_by_barn[device.barn_id].append(payload)
            else:
                sensors_by_farm[device.farm_id].append(payload)

        farms_payload = []
        for farm in farms_qs:
            barns_payload = []
            for barn in barns_by_farm.get(farm.id, []):
                zones_payload = []
                for zone in zones_by_barn.get(barn.id, []):
                    zone_sensors = sensors_by_zone.get(zone.id, [])
                    zones_payload.append(
                        {
                            "id": zone.id,
                            "name": zone.name,
                            "code": zone.code,
                            "description": zone.description,
                            "sensor_count": len(zone_sensors),
                            "sensors": zone_sensors,
                        }
                    )

                barn_sensors = sensors_by_barn.get(barn.id, [])
                barns_payload.append(
                    {
                        "id": barn.id,
                        "name": barn.name,
                        "code": barn.code,
                        "description": barn.description,
                        "sensor_count": len(barn_sensors) + sum(z["sensor_count"] for z in zones_payload),
                        "sensors": barn_sensors,
                        "zones": zones_payload,
                    }
                )

            farm_level_sensors = sensors_by_farm.get(farm.id, [])
            farms_payload.append(
                {
                    "id": farm.id,
                    "name": farm.name,
                    "code": farm.code,
                    "location": farm.location,
                    "sensor_count": len(farm_level_sensors)
                    + sum(barn["sensor_count"] for barn in barns_payload),
                    "sensors": farm_level_sensors,
                    "barns": barns_payload,
                }
            )

        return Response({"farms": farms_payload})
