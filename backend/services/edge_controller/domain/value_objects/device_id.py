from dataclasses import dataclass

from ..exceptions.validation_error import DomainValidationError


@dataclass(frozen=True)
class DeviceId:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise DomainValidationError("DeviceId cannot be empty")
