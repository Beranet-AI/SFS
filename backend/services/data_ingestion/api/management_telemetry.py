from fastapi import APIRouter
from typing import Dict, Any

from backend.services.data_ingestion.application.services.ingest_service import (
    IngestService,
)
from backend.services.data_ingestion.application.services.rule_dispatcher import (
    RuleDispatcher,
)
from backend.services.data_ingestion.application.use_cases.ReceiveTelemetry.use_case import (
    ReceiveTelemetryUseCase,
)
from backend.services.data_ingestion.application.use_cases.ReceiveTelemetry.receive_telemetry_input import (
    ReceiveTelemetryInput,
)
from backend.services.data_ingestion.application.use_cases.RequestValidation.use_case import (
    RequestValidationUseCase,
)
from backend.services.data_ingestion.application.use_cases.RequestValidation.request_validation_input import (
    RequestValidationInput,
)

router = APIRouter(prefix="/management-telemetry", tags=["management-telemetry"])

_ingest = IngestService()
_rules = RuleDispatcher()
_receive_uc = ReceiveTelemetryUseCase()
_validate_uc = RequestValidationUseCase()


@router.post("/telemetry")
def ingest_telemetry(payload: Dict[str, Any]):
    received = _receive_uc.execute(ReceiveTelemetryInput(payload=payload))
    validation = _validate_uc.execute(
        RequestValidationInput(payload=received.payload)
    )

    if not validation.valid:
        return {"ok": False, "details": validation.details}

    _ingest.push_livestatus(received.payload)
    _rules.dispatch(received.payload)

    return {"ok": True}
