import requests
from ai_decision.core.config import TELEMETRY_BASE
from ai_decision.domain.inputs.telemetry_window import TelemetryWindow, TelemetryPoint
from datetime import datetime

class TelemetryClient:
    """
    Pulls telemetry history from management service.
    """

    def fetch_window(self, livestock_id: str, limit: int = 50) -> TelemetryWindow:
        url = f"{TELEMETRY_BASE}/recent/{livestock_id}/"
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        raw = r.json()

        points = [
            TelemetryPoint(
                metric=p["metric"],
                value=float(p["value"]),
                recorded_at=datetime.fromisoformat(p["recorded_at"]),
            )
            for p in raw
        ]

        return TelemetryWindow(
            livestock_id=livestock_id,
            points=points,
        )
