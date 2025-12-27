from backend.shared.enums.health_state import HealthState

class SimpleHealthModel:
    """
    Placeholder ML model (rule-based).
    Replace with real ML (PyTorch/ONNX).
    """

    def predict(self, window) -> float:
        if not window.points:
            return 1.0

        avg = sum(p.value for p in window.points) / len(window.points)
        # normalize example
        return max(0.0, min(1.0, 1.0 - avg / 100))

    def map_score_to_state(self, score: float) -> HealthState:
        if score >= 0.85:
            return HealthState.HEALTHY
        if score >= 0.65:
            return HealthState.AT_RISK
        if score >= 0.4:
            return HealthState.SICK
        return HealthState.CRITICAL
