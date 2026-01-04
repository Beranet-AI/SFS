from apps.commands.domain.enums.command_status import CommandStatus
from apps.commands.domain.repositories.discovered_device_repository import (
    DiscoveredDeviceRepository,
)
from apps.commands.domain.repositories.discovery_session_repository import (
    DiscoverySessionRepository,
)


class DiscoveryResultService:
    """
    Persist discovery output from async command results.

    This is invoked from ReceiveResultUseCase after the command lifecycle
    is updated so that discovery stays asynchronous and side-effect-safe.
    """

    def __init__(
        self,
        *,
        session_repository: DiscoverySessionRepository,
        device_repository: DiscoveredDeviceRepository,
    ) -> None:
        self._session_repository = session_repository
        self._device_repository = device_repository

    def handle_result(
        self, *, command_id: str, status: CommandStatus, result: dict
    ) -> None:
        session = self._session_repository.get_by_command_id(command_id=command_id)
        if not session:
            return

        devices = self._extract_devices(result)

        if status == CommandStatus.SUCCEEDED:
            self._session_repository.mark_completed(
                session_id=session.id,
                device_count=len(devices),
            )
        elif status == CommandStatus.FAILED:
            self._session_repository.mark_failed(
                session_id=session.id,
                error_message=result.get("error_message", ""),
            )

        for payload in devices:
            device_id = (
                payload.get("device_serial")
                or payload.get("device_id")
                or payload.get("serial")
                or ""
            )
            if not device_id:
                continue

            self._device_repository.upsert(
                session_id=session.id,
                device_id=device_id,
                device_type=payload.get("device_type") or payload.get("type") or "",
                ip_address=payload.get("ip_address") or payload.get("ip"),
                capabilities=payload.get("capabilities") or {},
                raw_payload=payload,
            )

    @staticmethod
    def _extract_devices(result: dict) -> list[dict]:
        devices = result.get("devices")
        if isinstance(devices, list):
            return devices
        return []
