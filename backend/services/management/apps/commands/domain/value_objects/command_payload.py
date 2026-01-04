from dataclasses import dataclass
from typing import Any, Dict

from apps.commands.domain.exceptions.command_exceptions import CommandValidationError


@dataclass(frozen=True)
class CommandPayload:
    data: Dict[str, Any]

    @classmethod
    def from_raw(cls, raw: Dict[str, Any] | None) -> "CommandPayload":
        if raw is None:
            return cls(data={})
        if not isinstance(raw, dict):
            raise CommandValidationError("payload must be a JSON object")
        return cls(data=raw)
