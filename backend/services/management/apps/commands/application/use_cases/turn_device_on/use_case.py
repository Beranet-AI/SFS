from typing import Protocol

from apps.commands.application.use_cases.send_command.input_dto import (
    SendCommandInputDTO,
)
from apps.commands.application.use_cases.send_command.use_case import (
    SendCommandUseCase,
)
from apps.commands.domain.enums.command_target_kind import CommandTargetKind
from apps.commands.domain.enums.command_type import CommandType
from apps.commands.domain.exceptions.command_exceptions import CommandValidationError
from apps.commands.domain.repositories.command_repository import CommandRepository
from apps.devices.application.services.device_service import DeviceService
from apps.devices.models import DeviceStatus
from .input_dto import TurnDeviceOnInputDTO


class EdgeControllerClient(Protocol):
    def publish_command(self, *, edge_id: str, command: dict) -> None:
        ...


class TurnDeviceOnUseCase:
    """
    Turn a device on using the ON_OFF command.
    """

    def __init__(
        self,
        *,
        command_repository: CommandRepository,
        edge_client: EdgeControllerClient,
        device_service: DeviceService | None = None,
    ) -> None:
        self._device_service = device_service or DeviceService()
        self._send_command_use_case = SendCommandUseCase(
            repository=command_repository,
            edge_client=edge_client,
        )

    def execute(
        self, dto: TurnDeviceOnInputDTO, *, created_by: str
    ):
        device = self._device_service.get_by_id(device_id=dto.device_id)
        if device.status == DeviceStatus.DISABLED:
            raise CommandValidationError("Device is disabled and cannot be turned on.")

        edge_node_id = (
            (device.metadata or {}).get("edge_node_id")
            or (device.metadata or {}).get("edge_id")
        )

        return self._send_command_use_case.execute(
            SendCommandInputDTO(
                command_name=CommandType.ON_OFF.value,
                target_kind=CommandTargetKind.DEVICE.value,
                target_id=device.serial,
                edge_node_id=edge_node_id,
                payload={"device_id": device.serial, "action": "ON"},
            ),
            created_by=created_by,
        )
