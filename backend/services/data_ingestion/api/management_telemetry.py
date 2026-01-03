from typing import Any, Dict

from fastapi import APIRouter

from backend.services.data_ingestion.api.base import BaseController
from backend.services.data_ingestion.application.services.ingest_service import (
    IngestService,
)
from backend.services.data_ingestion.application.services.rule_dispatcher import (
    RuleDispatcher,
)
from backend.services.data_ingestion.application.use_cases.recieve_telemetry.use_case import (
    ReceiveTelemetryUseCase,
)
from backend.services.data_ingestion.application.use_cases.recieve_telemetry.input_dto import (
    ReceiveTelemetryInput,
)
from backend.services.data_ingestion.application.use_cases.request_validation.use_case import (
    RequestValidationUseCase,
)
from backend.services.data_ingestion.application.use_cases.request_validation.input_dto import (
    RequestValidationInput,
)
from backend.services.data_ingestion.api.management_telemetry_schema import (
    TelemetryIngestSchema,
)

router = APIRouter(prefix="/management-telemetry", tags=["management-telemetry"])

_ingest = IngestService()
_rules = RuleDispatcher()
_receive_uc = ReceiveTelemetryUseCase()
_validate_uc = RequestValidationUseCase()


class ManagementTelemetryController(BaseController):
    def __init__(
        self,
        ingest: IngestService,
        rules: RuleDispatcher,
        receive_uc: ReceiveTelemetryUseCase,
        validate_uc: RequestValidationUseCase,
    ) -> None:
        self._ingest = ingest
        self._rules = rules
        self._receive_uc = receive_uc
        self._validate_uc = validate_uc

    def ingest_telemetry(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        validated = self.validate_payload(payload, TelemetryIngestSchema)
        received = self._receive_uc.execute(
            ReceiveTelemetryInput(payload=validated.dict())
        )
        validation = self._validate_uc.execute(
            RequestValidationInput(payload=received.payload)
        )

        if not validation.valid:
            return self.response_error(validation.details)

        self._ingest.push_livestatus(received.payload)
        self._rules.dispatch(received.payload)

        return self.response_ok()


controller = ManagementTelemetryController(
    ingest=_ingest,
    rules=_rules,
    receive_uc=_receive_uc,
    validate_uc=_validate_uc,
)


@router.post("/telemetry")
def ingest_telemetry(payload: Dict[str, Any]):
    return controller.ingest_telemetry(payload)
