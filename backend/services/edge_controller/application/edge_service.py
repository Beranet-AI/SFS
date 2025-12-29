from ..application.use_cases.execute_command.use_case import ExecuteCommandUseCase

from ..application.use_cases.report_command_result.use_case import (
    ReportCommandResultUseCase,
)
from ..application.use_cases.forward_telemetry.use_case import ForwardTelemetryUseCase

from ..infrastructure.mqtt.device_client import DeviceClient
from ..infrastructure.clients.management_client import ManagementClient
from ..infrastructure.clients.data_ingestion_client import DataIngestionClient

from ..application.use_cases.execute_command.input_dto import ExecuteCommandInputDTO
from ..application.use_cases.forward_telemetry.input_dto import TelemetryInputDTO


class EdgeService:
    """
    Single orchestration point for edge_controller
    """

    def __init__(self):
        # Infrastructure dependencies
        self._device_client = DeviceClient()
        self._management_client = ManagementClient()
        self._data_ingestion_client = DataIngestionClient()

        # Use cases
        self._execute_command_uc = ExecuteCommandUseCase(
            device_client=self._device_client
        )
        self._report_result_uc = ReportCommandResultUseCase(
            management_client=self._management_client
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

        # 1️⃣ Execute
        result_dto = self._execute_command_uc.execute(command_dto)

        # 2️⃣ Report to management (fire & forget or sync)
        self._report_result_uc.execute(
            result_dto=result_dto.__dict__
        )

        # 3️⃣ Return result
        return result_dto

    # =====================================================
    # TELEMETRY FLOW (Device → Edge → Data Ingestion)
    # =====================================================
    def handle_telemetry(self, telemetry_dto: TelemetryInputDTO):
        """
        Forward telemetry from approved devices to data_ingestion
        """
        self._forward_telemetry_uc.execute(telemetry_dto)
