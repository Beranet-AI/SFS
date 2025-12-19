from fastapi import APIRouter
from datetime import datetime
from data_ingestion.api.schemas import TelemetryIngestSchema
from data_ingestion.domain.telemetry_event import TelemetryEvent
from data_ingestion.application.services.ingest_service import IngestService
from data_ingestion.application.services.rule_dispatcher import RuleDispatcher
from data_ingestion.infrastructure.clients.management_client import ManagementClient
from data_ingestion.infrastructure.clients.monitoring_client import MonitoringClient
from data_ingestion.infrastructure.clients.rules_client import RulesClient

router = APIRouter()

@router.post("/telemetry/ingest/")
def ingest(payload: TelemetryIngestSchema):
    event = TelemetryEvent(
        device_id=payload.device_id,
        livestock_id=payload.livestock_id,
        metric=payload.metric,
        value=payload.value,
        recorded_at=payload.recorded_at or datetime.utcnow(),
    )

    svc = IngestService(
        management_client=ManagementClient(),
        monitoring_client=MonitoringClient(),
        rule_dispatcher=RuleDispatcher(RulesClient()),
    )
    svc.ingest(event)
    return {"ok": True}
