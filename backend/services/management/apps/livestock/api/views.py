from rest_framework.views import APIView
from rest_framework.response import Response
from apps.livestock.infrastructure.models.livestock_model import LivestockModel
from apps.livestock.infrastructure.repositories.livestock_repo_impl import DjangoLivestockRepository
from apps.livestock.application.use_cases.update_health import UpdateHealthUseCase

class LivestockView(APIView):
    def get(self, request):
        qs = LivestockModel.objects.all().values(
            "id","tag","farm_id","barn","zone","health_state","health_confidence","health_evaluated_at"
        )
        return Response(list(qs))

class LivestockHealthEvalView(APIView):
    repo = DjangoLivestockRepository()

    def post(self, request, livestock_id: str):
        score = float(request.data.get("score", 1.0))
        uc = UpdateHealthUseCase(self.repo)
        livestock = uc.execute(livestock_id=livestock_id, score=score)
        return Response({
            "id": livestock.id,
            "health_state": livestock.health_status.state.value,
            "health_confidence": livestock.health_status.confidence,
            "health_evaluated_at": livestock.health_status.evaluated_at,
        })
