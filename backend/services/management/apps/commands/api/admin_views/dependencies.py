from apps.commands.application.services.command_dispatcher import CommandDispatcher
from apps.commands.application.use_cases.get_command.use_case import (
    GetCommandUseCase,
)
from apps.commands.application.use_cases.receive_result.use_case import (
    ReceiveResultUseCase,
)
from apps.commands.application.use_cases.send_command.use_case import (
    SendCommandUseCase,
)
from apps.commands.application.use_cases.start_network_scan.use_case import (
    StartNetworkScanUseCase,
)
from apps.commands.infrastructure.clients.edge_controller_client import (
    EdgeControllerClient,
)
from apps.commands.infrastructure.executors.device_command_executor import (
    DeviceCommandExecutor,
)
from apps.commands.infrastructure.executors.edge_command_executor import (
    EdgeCommandExecutor,
)
from apps.commands.infrastructure.repositories.django_capability_repository import (
    DjangoCapabilityRepository,
)
from apps.commands.infrastructure.repositories.django_command_repository import (
    DjangoCommandRepository,
)


def build_send_command_use_case() -> SendCommandUseCase:
    capability_repository = DjangoCapabilityRepository()
    edge_client = EdgeControllerClient()
    dispatcher = CommandDispatcher(
        edge_executor=EdgeCommandExecutor(edge_client=edge_client),
        device_executor=DeviceCommandExecutor(edge_client=edge_client),
        capability_repository=capability_repository,
    )
    return SendCommandUseCase(
        repository=DjangoCommandRepository(),
        dispatcher=dispatcher,
        capability_repository=capability_repository,
    )


def build_start_network_scan_use_case() -> StartNetworkScanUseCase:
    return StartNetworkScanUseCase(
        send_command_use_case=build_send_command_use_case()
    )


def build_receive_result_use_case() -> ReceiveResultUseCase:
    return ReceiveResultUseCase(
        command_repository=DjangoCommandRepository(),
    )


def build_get_command_use_case() -> GetCommandUseCase:
    return GetCommandUseCase(
        command_repository=DjangoCommandRepository(),
    )
