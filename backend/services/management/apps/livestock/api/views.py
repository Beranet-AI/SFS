from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.livestock.application.services.livestock_service import LivestockService
from apps.livestock.api.serializers import LivestockSerializer


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
