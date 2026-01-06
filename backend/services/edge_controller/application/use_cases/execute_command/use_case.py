from datetime import datetime, timezone
from typing import Callable, List

from ....domain.enums.command_status import CommandStatus
from ....domain.enums.command_type import CommandType
from ....domain.exceptions.validation_error import DomainValidationError
from ....infrastructure.clients.commands_client import CommandsClient
from ....infrastructure.mqtt.device_client import DeviceClient
from ....infrastructure.scanners.scan_local_network import scan_local_network
from .input_dto import ExecuteCommandInputDTO
from .output_dto import (
    BaseCommandResultDTO,
    DiscoverCommandResultDTO,
    OnOffCommandResultDTO,
    RebootCommandResultDTO,
)


class ExecuteCommandUseCase:
    """
    Execute management command on the edge and report the result upstream.
    """

    def __init__(
        self,
        *,
        device_client: DeviceClient,
        commands_client: CommandsClient,
        network_scanner: Callable[[], List[dict]] | None = None,
    ) -> None:
        self._device_client = device_client
        self._commands_client = commands_client
        self._network_scanner = network_scanner or scan_local_network

    def execute(self, dto: ExecuteCommandInputDTO) -> BaseCommandResultDTO:
        command_type = CommandType.from_raw(dto.command_type)
        executed_at = self._now_iso()

        if command_type is CommandType.DISCOVER:
            result = self._execute_discover(dto, executed_at)
        elif command_type is CommandType.ON_OFF:
            result = self._execute_on_off(dto, executed_at)
        elif command_type is CommandType.REBOOT:
            result = self._execute_reboot(dto, executed_at)
        else:
            raise DomainValidationError(
                f"Unsupported command_type: {dto.command_type}"
            )

        self._commands_client.send_command_result(
            self._build_result_payload(result)
        )

        return result

    def _execute_discover(
        self, dto: ExecuteCommandInputDTO, executed_at: str
    ) -> DiscoverCommandResultDTO:
        devices = self._network_scanner()

        return DiscoverCommandResultDTO(
            command_id=dto.command_id,
            command_type=CommandType.DISCOVER.value,
            status=CommandStatus.COMPLETED.value,
            executed_at=executed_at,
            devices=devices,
        )

    def _execute_on_off(
        self, dto: ExecuteCommandInputDTO, executed_at: str
    ) -> OnOffCommandResultDTO:
        payload = dto.payload
        device_id = payload.get("device_id")
        action = payload.get("action")

        if not device_id or action not in {"ON", "OFF"}:
            raise DomainValidationError("Invalid ON_OFF payload")

        success = self._device_client.send_on_off(
            device_id=device_id,
            action=action,
        )

        status = (
            CommandStatus.COMPLETED.value
            if success
            else CommandStatus.FAILED.value
        )

        return OnOffCommandResultDTO(
            command_id=dto.command_id,
            command_type=CommandType.ON_OFF.value,
            status=status,
            executed_at=executed_at,
            device_id=device_id,
            execution_state=action if success else CommandStatus.FAILED.value,
        )

    def _execute_reboot(
        self, dto: ExecuteCommandInputDTO, executed_at: str
    ) -> RebootCommandResultDTO:
        device_id = dto.payload.get("device_id")

        if not device_id:
            raise DomainValidationError("Invalid REBOOT payload")

        success = self._device_client.send_reboot(device_id)

        status = (
            CommandStatus.COMPLETED.value
            if success
            else CommandStatus.FAILED.value
        )

        return RebootCommandResultDTO(
            command_id=dto.command_id,
            command_type=CommandType.REBOOT.value,
            status=status,
            executed_at=executed_at,
            device_id=device_id,
            reboot_state="REBOOTED" if success else CommandStatus.FAILED.value,
        )

    @staticmethod
    def _build_result_payload(result: BaseCommandResultDTO) -> dict:
        payload = {
            "command_id": result.command_id,
            "command_type": result.command_type,
            "status": result.status,
            "executed_at": result.executed_at,
        }

        if isinstance(result, DiscoverCommandResultDTO):
            payload["payload"] = {"devices": result.devices}
        elif isinstance(result, OnOffCommandResultDTO):
            payload["payload"] = {
                "device_id": result.device_id,
                "execution_state": result.execution_state,
            }
        elif isinstance(result, RebootCommandResultDTO):
            payload["payload"] = {
                "device_id": result.device_id,
                "reboot_state": result.reboot_state,
            }
        else:
            raise DomainValidationError(
                f"Unsupported result type: {type(result).__name__}"
            )

        return payload

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
