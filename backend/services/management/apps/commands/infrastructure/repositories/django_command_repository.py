from django.utils import timezone

from apps.commands.domain.entities.command import Command
from apps.commands.domain.entities.command_execution import CommandExecution
from apps.commands.domain.enums.command_status import CommandStatus
from apps.commands.domain.repositories.command_repository import CommandRepository
from apps.commands.infrastructure.mappers.command_mapper import CommandMapper
from apps.commands.infrastructure.mappers.scan_result_mapper import ScanResultMapper
from apps.commands.infrastructure.models.command_execution_model import (
    CommandAttemptModel,
)
from apps.commands.infrastructure.models.command_model import (
    CommandModel,
    CommandStatusChoices,
)
from apps.commands.infrastructure.models.network_scan_result_model import (
    NetworkScanResultModel,
)


class DjangoCommandRepository(CommandRepository):
    def create(self, *, data: dict, created_by: str) -> Command:
        command = CommandModel.objects.create(
            **data,
            status=CommandStatusChoices.PENDING,
            created_by=created_by or "manual",
        )
        return CommandMapper.to_domain(command)

    def get(self, *, command_id: str) -> Command:
        command = CommandModel.objects.get(id=command_id)
        return CommandMapper.to_domain(command)

    def mark_acked(self, *, command_id: str, meta: dict | None = None) -> Command:
        command = CommandModel.objects.get(id=command_id)
        command.mark_acked(meta=meta)
        return CommandMapper.to_domain(command)

    def mark_dispatched(self, *, command_id: str) -> Command:
        command = CommandModel.objects.get(id=command_id)
        command.mark_dispatched()
        return CommandMapper.to_domain(command)

    def mark_result(
        self,
        *,
        command_id: str,
        status: CommandStatus,
        result: dict | None = None,
        error_code: str = "",
        error_message: str = "",
    ) -> Command:
        command = CommandModel.objects.get(id=command_id)

        if status == CommandStatus.SUCCEEDED:
            command.mark_succeeded(result=result)
        elif status == CommandStatus.FAILED:
            command.mark_failed(code=error_code, message=error_message, result=result)
        else:
            command.status = status.value
            command.finished_at = timezone.now()
            command.last_result = result or {}
            command.last_error_code = error_code or ""
            command.last_error_message = error_message or ""
            command.save(
                update_fields=[
                    "status",
                    "finished_at",
                    "last_result",
                    "last_error_code",
                    "last_error_message",
                ]
            )

        return CommandMapper.to_domain(command)

    def record_execution_ack(
        self,
        *,
        command_id: str,
        attempt_no: int,
        executor_receipt: str | None = None,
        meta: dict | None = None,
    ) -> CommandExecution:
        command = CommandModel.objects.get(id=command_id)
        attempt, _ = CommandAttemptModel.objects.get_or_create(
            command=command,
            attempt_no=attempt_no,
            defaults={"status": "sent", "dispatched_at": timezone.now()},
        )
        attempt.executor_receipt = executor_receipt or ""
        attempt.acked_at = timezone.now()
        attempt.status = "acked"
        attempt.debug = {**(attempt.debug or {}), "ack_meta": meta or {}}
        attempt.save(update_fields=["executor_receipt", "acked_at", "status", "debug"])
        return CommandExecution(
            id=str(attempt.id),
            command_id=str(command.id),
            attempt_no=attempt.attempt_no,
            status=attempt.status,
            created_at=attempt.created_at,
            dispatched_at=attempt.dispatched_at,
            acked_at=attempt.acked_at,
            result_at=attempt.result_at,
            executor_receipt=attempt.executor_receipt,
            debug=attempt.debug,
        )

    def record_execution_result(
        self,
        *,
        command_id: str,
        attempt_no: int,
        status: str,
        result: dict | None = None,
        error_code: str = "",
        error_message: str = "",
        meta: dict | None = None,
    ) -> CommandExecution:
        command = CommandModel.objects.get(id=command_id)
        attempt, _ = CommandAttemptModel.objects.get_or_create(
            command=command,
            attempt_no=attempt_no,
            defaults={"status": "sent", "dispatched_at": timezone.now()},
        )

        attempt.result_at = timezone.now()
        attempt.debug = {
            **(attempt.debug or {}),
            "result_meta": meta or {},
            "error_code": error_code,
            "error_message": error_message,
            "result": result or {},
        }
        attempt.status = status
        attempt.save(update_fields=["result_at", "status", "debug"])
        return CommandExecution(
            id=str(attempt.id),
            command_id=str(command.id),
            attempt_no=attempt.attempt_no,
            status=attempt.status,
            created_at=attempt.created_at,
            dispatched_at=attempt.dispatched_at,
            acked_at=attempt.acked_at,
            result_at=attempt.result_at,
            executor_receipt=attempt.executor_receipt,
            debug=attempt.debug,
        )

    def record_scan_result(self, *, scan_id: str, device_uid: str, payload: dict) -> None:
        mapped = ScanResultMapper.to_model_data(payload)
        if not mapped.get("device_uid"):
            mapped["device_uid"] = device_uid
        mapped["scan_id"] = scan_id

        device, created = NetworkScanResultModel.objects.get_or_create(
            scan_id=scan_id,
            device_uid=mapped["device_uid"],
            defaults=mapped,
        )
        if not created:
            for field in [
                "device_name",
                "device_category",
                "device_type",
                "protocol",
                "adapter_type",
                "direction",
                "supports_commands",
                "supported_command_categories",
                "ip_address",
                "port",
                "network_address",
                "signal_strength",
                "firmware_version",
                "vendor",
                "model",
                "battery_level",
                "last_seen_at",
                "discovered_at",
                "scan_status",
                "raw_capabilities",
            ]:
                setattr(device, field, mapped[field])
            device.save(
                update_fields=[
                    "device_name",
                    "device_category",
                    "device_type",
                    "protocol",
                    "adapter_type",
                    "direction",
                    "supports_commands",
                    "supported_command_categories",
                    "ip_address",
                    "port",
                    "network_address",
                    "signal_strength",
                    "firmware_version",
                    "vendor",
                    "model",
                    "battery_level",
                    "last_seen_at",
                    "discovered_at",
                    "scan_status",
                    "raw_capabilities",
                    "updated_at",
                ]
            )
