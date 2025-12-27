"""
MQTT adapter (optional).
Bridges MQTT messages into IngestService.
"""

import json
from datetime import datetime
from backend.services.data_ingestion.domain.telemetry_event import TelemetryEvent

class MQTTAdapter:
    def __init__(self, ingest_service):
        self.ingest_service = ingest_service

    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode())
        event = TelemetryEvent(
            device_id=payload["device_id"],
            livestock_id=payload["livestock_id"],
            metric=payload["metric"],
            value=float(payload["value"]),
            recorded_at=datetime.fromisoformat(payload["recorded_at"]),
        )
        self.ingest_service.ingest(event)
