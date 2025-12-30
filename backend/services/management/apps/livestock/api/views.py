from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.livestock.application.services.livestock_service import LivestockService
from apps.livestock.api.serializers import (
    LivestockSerializer,
    LivestockSensorGroupSerializer,
)
from apps.livestock.application.use_cases.register_sensor_group.use_case import (
    RegisterLivestockSensorGroupUseCase,
)
from apps.livestock.mappers.sensor_group_mapper import (
    LivestockSensorGroupMapper,
)


class LivestockView(APIView):
    service = LivestockService()

    def get(self, request):
        qs = self.service.list_all()
        return Response(LivestockSerializer(qs, many=True).data)

    def post(self, request):
        livestock = self.service.create(**request.data)
        return Response(
            LivestockSerializer(livestock).data,
            status=status.HTTP_201_CREATED,
        )


class LivestockHealthEvalView(APIView):
    service = LivestockService()

    def post(self, request, livestock_id: str):
        score = float(request.data.get("score", 1.0))

        livestock = self.service.update_health_from_score(
            livestock_id=livestock_id,
            score=score,
        )

        return Response(
            LivestockSerializer(livestock).data,
            status=status.HTTP_200_OK,
        )


class LivestockSensorGroupView(APIView):
    use_case = RegisterLivestockSensorGroupUseCase()

    def post(self, request):
        ser = LivestockSensorGroupSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        input_dto = LivestockSensorGroupMapper.from_payload(
            ser.validated_data
        )
        result = self.use_case.execute(input_dto)

        return Response(
            LivestockSensorGroupMapper.to_response(result),
            status=status.HTTP_201_CREATED,
        )
