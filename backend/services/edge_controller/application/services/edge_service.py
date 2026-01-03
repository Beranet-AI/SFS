from datetime import timezone

from ..use_cases.execute_command.use_case import ExecuteCommandUseCase
from ..use_cases.send_result.use_case import SendResultUseCase
from ..use_cases.CheckDeviceRegistered.use_case import CheckDeviceRegisteredUseCase
from ..use_cases.ValidateRawTelemetry.use_case import ValidateRawTelemetryUseCase

from ...infrastructure.mqtt.device_client import DeviceClient
from ...infrastructure.clients.commands_client import CommandsClient
from ...infrastructure.clients.management_telemetry_client import (
    ManagementTelemetryClient,
)

from ..use_cases.execute_command.input_dto import (
    ExecuteCommandInputDTO,
)
from ..use_cases.forward_telemetry.input_dto import (
    TelemetryInputDTO,
)
from ..use_cases.CheckDeviceRegistered.check_device_registered_input import (
    CheckDeviceRegisteredInput,
)
from ..use_cases.ValidateRawTelemetry.validate_raw_telemetry_input import (
    ValidateRawTelemetryInput,
)

from ...infrastructure.mappers.result_mapper import InboundResultMapper


class EdgeService:
    """
    Single orchestration point for edge_controller
    """

    def __init__(self):
        # Infrastructure
        self._device_client = DeviceClient()
        self._commands_client = CommandsClient()
        self._management_telemetry_client = ManagementTelemetryClient()

        # Use cases
        self._execute_command_uc = ExecuteCommandUseCase(
            device_client=self._device_client
        )
        self._report_result_uc = SendResultUseCase(
            commands_client=self._commands_client
        )
        self._check_device_uc = CheckDeviceRegisteredUseCase()
        self._validate_raw_uc = ValidateRawTelemetryUseCase()

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
        check_result = self._check_device_uc.execute(
            CheckDeviceRegisteredInput(device_id=telemetry_dto.device_id)
        )
        if not check_result.is_registered:
            raise ValueError("Device is not registered")

        self._validate_raw_uc.execute(
            ValidateRawTelemetryInput(payload=telemetry_dto.to_dict())
        )
        self._management_telemetry_client.send_raw_telemetry(
            telemetry_dto.to_dict()
        )
