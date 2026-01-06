from ....application.use_cases.execute_command.use_case import ExecuteCommandUseCase
from ....application.use_cases.receive_telemetry.use_case import (
    ReceiveTelemetryUseCase,
)
from ....infrastructure.clients.commands_client import CommandsClient
from ....infrastructure.clients.management_telemetry_client import (
    ManagementTelemetryClient,
)
from ....infrastructure.mqtt.device_client import DeviceClient
from ....infrastructure.repositories.device_registry import (
    InMemoryDeviceRegistry,
)


_registry = InMemoryDeviceRegistry()


def get_execute_command_use_case() -> ExecuteCommandUseCase:
    return ExecuteCommandUseCase(
        device_client=DeviceClient(),
        commands_client=CommandsClient(),
    )


def get_receive_telemetry_use_case() -> ReceiveTelemetryUseCase:
    return ReceiveTelemetryUseCase(
        device_registry=_registry,
        telemetry_client=ManagementTelemetryClient(),
    )
