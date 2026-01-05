from apps.commands.domain.exceptions.invalid_target import InvalidTargetError
from apps.commands.domain.exceptions.unsupported_command import (
    UnsupportedCommandError,
)
from apps.commands.domain.repositories.capability_repository import CapabilityRepository


class IsCommandAllowed:
    def __init__(self, *, capability_repository: CapabilityRepository) -> None:
        self._capability_repository = capability_repository

    def validate(
        self,
        *,
        command_type: str,
        device_category: str | None,
        device_type: str | None,
    ) -> None:
        capabilities = self._capability_repository.list_capabilities()
        if not capabilities:
            return

        if device_category is None or device_type is None:
            return

        matches = [
            capability
            for capability in capabilities
            if capability.command_type == command_type
            and capability.device_category == device_category
            and capability.device_type == device_type
        ]
        if not matches:
            known_commands = {capability.command_type for capability in capabilities}
            if command_type not in known_commands:
                raise UnsupportedCommandError(
                    f"Unsupported command_type: {command_type}"
                )
            raise InvalidTargetError(
                "Command is not supported for the selected device category/type."
            )
