from apps.commands.application.services.command_tracker import CommandTracker
from apps.commands.domain.enums.command_status import CommandStatus
from apps.commands.domain.enums.command_type import CommandType
from apps.commands.domain.repositories.command_repository import CommandRepository
from .input_dto import ReceiveResultInputDTO
from .output_dto import ReceiveResultOutputDTO


class ReceiveResultUseCase:
    def __init__(self, *, command_repository: CommandRepository) -> None:
        self._command_repository = command_repository
        self._tracker = CommandTracker(command_repository=command_repository)

    def execute(self, dto: ReceiveResultInputDTO) -> ReceiveResultOutputDTO:
        status = CommandStatus.from_value(dto.status)
        self._tracker.record_result(
            command_id=dto.command_id,
            attempt_no=dto.attempt_no,
            status=status,
            result=dto.result,
            error_code=dto.error_code,
            error_message=dto.error_message,
            meta=dto.meta,
        )

        command = self._command_repository.get(command_id=dto.command_id)
        if command.command_name == CommandType.GET_CONNECTED_DEVICES.value:
            result_payload = dict(dto.result or {})
            if "devices" not in result_payload and dto.meta:
                if isinstance(dto.meta.get("devices"), list):
                    result_payload["devices"] = dto.meta["devices"]
            self._record_scan_results(result_payload)

        return ReceiveResultOutputDTO(command_id=dto.command_id, status=status.value)

    def _record_scan_results(self, result_payload: dict) -> None:
        scan_id = result_payload.get("scan_id")
        if not scan_id:
            return
        devices = result_payload.get("devices")
        if not isinstance(devices, list):
            return

        for payload in devices:
            device_uid = str(payload.get("device_uid") or payload.get("device_id") or "")
            if not device_uid:
                continue
            self._command_repository.record_scan_result(
                scan_id=str(scan_id),
                device_uid=device_uid,
                payload=payload,
            )
