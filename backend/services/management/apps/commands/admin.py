"""Register infrastructure admin classes for the commands app."""

from apps.commands.infrastructure.admin import CommandAdmin, CommandAttemptAdmin

__all__ = ["CommandAdmin", "CommandAttemptAdmin"]
