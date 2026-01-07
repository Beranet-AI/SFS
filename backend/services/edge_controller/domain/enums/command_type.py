from enum import Enum

from ..exceptions.validation_error import DomainValidationError


class CommandType(str, Enum):
    DISCOVER = "DISCOVER"
    ON_OFF = "ON_OFF"
    REBOOT = "REBOOT"

    @classmethod
    def from_raw(cls, value: str) -> "CommandType":
        if value in {"get_connected_devices", "GET_CONNECTED_DEVICES"}:
            return cls.DISCOVER
        try:
            return cls(value)
        except ValueError as exc:
            raise DomainValidationError(
                f"Unsupported command_type: {value}"
            ) from exc
