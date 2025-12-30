from datetime import datetime, timezone

from .input_dto import ExecuteCommandInputDTO
from .output_dto import (
    DiscoverCommandResultDTO,
    OnOffCommandResultDTO,
    RebootCommandResultDTO,
)
from ....infrastructure.scanners.scan_local_network import scan_local_network
from ....infrastructure.mqtt.device_client import DeviceClient


class ExecuteCommandUseCase:
    """
    Edge-side command executor.
    Stateless. No domain entities.
    """

    def __init__(self, device_client: DeviceClient):
        self.device_client = device_client

    def execute(self, dto: ExecuteCommandInputDTO):
        """
        Dispatch execution based on command_type
        """
        received_at = datetime.now(timezone.utc)

        if dto.command_type == "DISCOVER":
            return self._execute_discover(dto)

        if dto.command_type == "ON_OFF":
            return self._execute_on_off(dto)

        if dto.command_type == "REBOOT":
            return self._execute_reboot(dto)

        raise ValueError(f"Unsupported command_type: {dto.command_type}")

    # ------------------------
    # DISCOVER
    # ------------------------
    def _execute_discover(self, dto: ExecuteCommandInputDTO):
        devices = scan_local_network()

        return DiscoverCommandResultDTO(
            command_id=dto.command_id,
            command_type="DISCOVER",
            status="COMPLETED",
            executed_at=datetime.now(timezone.utc),
            devices=devices,
        )

    # ------------------------
    # ON / OFF
    # ------------------------
    def _execute_on_off(self, dto: ExecuteCommandInputDTO):
        payload = dto.payload
        device_id = payload["device_id"]
        action = payload["action"]

        success = self.device_client.send_on_off(
            device_id=device_id,
            action=action,
        )

        return OnOffCommandResultDTO(
            command_id=dto.command_id,
            command_type="ON_OFF",
            status="COMPLETED" if success else "FAILED",
            executed_at=datetime.now(timezone.utc),
            device_id=device_id,
            execution_state=action if success else "FAILED",
        )

    # ------------------------
    # REBOOT
    # ------------------------
    def _execute_reboot(self, dto: ExecuteCommandInputDTO):
        device_id = dto.payload["device_id"]

        success = self.device_client.send_reboot(device_id)

        return RebootCommandResultDTO(
            command_id=dto.command_id,
            command_type="REBOOT",
            status="COMPLETED" if success else "FAILED",
            executed_at=datetime.now(timezone.utc),
            device_id=device_id,
            reboot_state="REBOOTED" if success else "FAILED",
        )
