from rest_framework.views import APIView
from rest_framework.response import Response
from apps.farms.infrastructure.repositories.farm_repo_impl import DjangoFarmRepository
from apps.farms.application.use_cases.create_farm import CreateFarmUseCase

class FarmsView(APIView):
    repo = DjangoFarmRepository()

    def get(self, request):
        return Response({"detail": "farms endpoint"})

    def post(self, request):
        uc = CreateFarmUseCase(self.repo)
        created = uc.execute(id="tmp", name=request.data["name"])
        return Response({"id": created.id, "name": created.name})
