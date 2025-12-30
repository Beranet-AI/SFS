from datetime import timezone

from ..use_cases.execute_command.use_case import ExecuteCommandUseCase
from ..use_cases.send_result.use_case import SendResultUseCase
from ..use_cases.forward_telemetry.use_case import ForwardTelemetryUseCase

from ...infrastructure.mqtt.device_client import DeviceClient
from ...infrastructure.clients.commands_client import CommandsClient
from ...infrastructure.clients.data_ingestion_client import DataIngestionClient

from ..use_cases.execute_command.input_dto import (
    ExecuteCommandInputDTO,
)
from ..use_cases.forward_telemetry.input_dto import (
    TelemetryInputDTO,
)

from ...mappers.result_mapper import InboundResultMapper


class EdgeService:
    """
    Single orchestration point for edge_controller
    """

    def __init__(self):
        # Infrastructure
        self._device_client = DeviceClient()
        self._commands_client = CommandsClient()
        self._data_ingestion_client = DataIngestionClient()

        # Use cases
        self._execute_command_uc = ExecuteCommandUseCase(
            device_client=self._device_client
        )
        self._report_result_uc = SendResultUseCase(
            commands_client=self._commands_client
        )
        self._forward_telemetry_uc = ForwardTelemetryUseCase(
            data_ingestion_client=self._data_ingestion_client
        )

    # =====================================================
    # COMMAND FLOW (Management → Edge → Management)
    # =====================================================
    def handle_command(self, command_dto: ExecuteCommandInputDTO):
        """
        1. Execute command
        2. Report result to management
        3. Return result for API response
        """

        # 1️⃣ Execute command
        result_dto = self._execute_command_uc.execute(command_dto)

        # 2️⃣ Map ResultDTO → SendResultInput
        report_dto = InboundResultMapper.to_input(result_dto)

        # 3️⃣ Report to management
        self._report_result_uc.execute(report_dto)

        # 4️⃣ Return result to API
        return result_dto

    # =====================================================
    # TELEMETRY FLOW (Device → Edge → Data Ingestion)
    # =====================================================
    def handle_telemetry(self, telemetry_dto: TelemetryInputDTO):
        self._forward_telemetry_uc.execute(telemetry_dto)
