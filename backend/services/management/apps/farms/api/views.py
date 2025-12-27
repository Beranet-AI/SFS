from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.farms.application.services.farm_service import FarmService
from .serializers import FarmSerializer


class FarmsView(APIView):
    service = FarmService()

    def get(self, request):
        farms = self.service.list_all()
        return Response(FarmSerializer(farms, many=True).data)

    def post(self, request):
        farm = self.service.create(name=request.data["name"])
        return Response(
            FarmSerializer(farm).data,
            status=status.HTTP_201_CREATED,
        )


class FarmDetailView(APIView):
    service = FarmService()

    def put(self, request, farm_id: int):
        farm = self.service.rename(
            farm_id=farm_id,
            name=request.data["name"],
        )
        return Response(FarmSerializer(farm).data)

    def delete(self, request, farm_id: int):
        self.service.delete(farm_id=farm_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
