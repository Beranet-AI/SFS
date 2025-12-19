from ai_decision.application.services.prediction_service import PredictionService

class DecisionPipeline:
    """
    End-to-end decision pipeline.
    """

    def __init__(self, telemetry_client, management_client, predictor: PredictionService):
        self.telemetry_client = telemetry_client
        self.management_client = management_client
        self.predictor = predictor

    def run(self, livestock_id: str):
        window = self.telemetry_client.fetch_window(livestock_id)
        prediction = self.predictor.predict(window)

        # push health update
        self.management_client.push_health_prediction(prediction)

        # optional: trigger incident if critical
        if prediction.state.value == "critical":
            self.management_client.create_incident(
                livestock_id,
                prediction.state,
                prediction.score,
            )

        return prediction
