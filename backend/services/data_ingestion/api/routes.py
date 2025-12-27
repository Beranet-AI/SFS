from fastapi import APIRouter
from typing import Dict, Any

from backend.services.data_ingestion.application.services.ingest_service import IngestService
from backend.services.data_ingestion.application.services.rule_dispatcher import RuleDispatcher

router = APIRouter(prefix="/ingest", tags=["ingest"])

_ingest = IngestService()
_rules = RuleDispatcher()


@router.post("/telemetry")
def ingest_telemetry(payload: Dict[str, Any]):
    # 1) realtime push
    _ingest.push_livestatus(payload)

    # 2) AI-ready rule dispatch
    _rules.dispatch(payload)

    return {"ok": True}
