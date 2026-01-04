class CommandDomainError(Exception):
    """Base exception for command domain errors."""


class CommandValidationError(CommandDomainError, ValueError):
    """Raised when command data violates domain rules."""
