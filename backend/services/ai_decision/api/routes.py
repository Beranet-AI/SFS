from fastapi import APIRouter
from backend.services.ai_decision.api.schemas import DecisionRequest
from backend.services.ai_decision.application.services.decision_pipeline import DecisionPipeline
from backend.services.ai_decision.application.services.prediction_service import PredictionService
from backend.services.ai_decision.infrastructure.clients.telemetry_client import TelemetryClient
from backend.services.ai_decision.infrastructure.clients.management_client import ManagementClient
from backend.services.ai_decision.infrastructure.models.simple_health_model import SimpleHealthModel

router = APIRouter()

_pipeline = DecisionPipeline(
    telemetry_client=TelemetryClient(),
    management_client=ManagementClient(),
    predictor=PredictionService(SimpleHealthModel()),
)

@router.post("/decision/health")
def run_decision(payload: DecisionRequest):
    prediction = _pipeline.run(payload.livestock_id)
    return {
        "livestock_id": prediction.livestock_id,
        "score": prediction.score,
        "state": prediction.state.value,
        "predicted_at": prediction.predicted_at,
    }
