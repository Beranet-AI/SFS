from dataclasses import dataclass

from apps.users.domain.exceptions.user_exceptions import UserDomainError


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if "@" not in self.value:
            raise UserDomainError("Invalid email address")
