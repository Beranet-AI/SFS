from apps.commands.domain.enums.command_target_kind import CommandTargetKind
from apps.commands.domain.exceptions.command_exceptions import CommandValidationError
from apps.commands.domain.value_objects.command_payload import CommandPayload


class CanSendCommand:
    def __init__(self, allowed_target_kinds: set[str] | None = None) -> None:
        self._allowed_target_kinds = allowed_target_kinds or {
            kind.value for kind in CommandTargetKind
        }

    def validate(
        self,
        *,
        command_name: str,
        target_kind: str,
        target_id: str,
        payload: dict | None,
        ack_deadline_sec: int | None,
        result_deadline_sec: int | None,
        max_attempts: int | None,
    ) -> None:
        if not command_name.strip():
            raise CommandValidationError("command_name is required")
        if target_kind not in self._allowed_target_kinds:
            raise CommandValidationError("target_kind is invalid")
        if not target_id.strip():
            raise CommandValidationError("target_id is required")

        CommandPayload.from_raw(payload)

        if ack_deadline_sec is not None and ack_deadline_sec <= 0:
            raise CommandValidationError("ack_deadline_sec must be positive")
        if result_deadline_sec is not None and result_deadline_sec <= 0:
            raise CommandValidationError("result_deadline_sec must be positive")
        if max_attempts is not None and max_attempts <= 0:
            raise CommandValidationError("max_attempts must be positive")
