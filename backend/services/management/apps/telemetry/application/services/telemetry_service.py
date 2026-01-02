# backend/services/management/apps/telemetry/application/services/telemetry_service.py

from ..use_cases.ReceiveRawTelemetry.use_case import ReceiveRawTelemetryUseCase
from ..use_cases.ReceiveRawTelemetry.receive_raw_telemetry_input import (
    ReceiveRawTelemetryInput,
)
from ..use_cases.StandardizeTelemetry.use_case import StandardizeTelemetryUseCase
from ..use_cases.StandardizeTelemetry.standardize_telemetry_input import (
    StandardizeTelemetryInput,
)
from ..use_cases.SendTelemetry.use_case import SendTelemetryUseCase
from ..use_cases.SendTelemetry.send_telemetry_input import SendTelemetryInput
from ..use_cases.RecordTelemetryEvent.use_case import RecordTelemetryEventUseCase
from ..use_cases.RecordTelemetryEvent.record_telemetry_event_input import (
    RecordTelemetryEventInput,
)


class TelemetryService:
    """
    Application Service (Orchestrator)

    Coordinates telemetry flow:
    - receive raw telemetry
    - standardize
    - send to ingestion
    - record event
    """

    def __init__(self):
        self._receive_uc = ReceiveRawTelemetryUseCase()
        self._standardize_uc = StandardizeTelemetryUseCase()
        self._send_uc = SendTelemetryUseCase()
        self._record_uc = RecordTelemetryEventUseCase()

    def receive_raw(self, payload: dict, source: str) -> dict:
        received = self._receive_uc.execute(
            ReceiveRawTelemetryInput(payload=payload, source=source)
        )
        standardized = self._standardize_uc.execute(
            StandardizeTelemetryInput(
                payload=received.payload, source=received.source
            )
        )
        self._send_uc.execute(
            SendTelemetryInput(standardized=standardized.standardized)
        )
        record_result = self._record_uc.execute(
            RecordTelemetryEventInput(standardized=standardized.standardized)
        )

        return {"recorded": record_result.recorded_count}
