from ai_decision.domain.outputs.health_prediction import HealthPrediction
from ai_decision.infrastructure.models.simple_health_model import SimpleHealthModel
from datetime import datetime

class PredictionService:
    """
    Runs ML model and produces prediction.
    """

    def __init__(self, model: SimpleHealthModel):
        self.model = model

    def predict(self, window) -> HealthPrediction:
        score = self.model.predict(window)
        state = self.model.map_score_to_state(score)

        return HealthPrediction(
            livestock_id=window.livestock_id,
            score=score,
            state=state,
            predicted_at=datetime.utcnow(),
        )
