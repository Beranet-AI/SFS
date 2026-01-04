"""Register infrastructure admin classes for the commands app."""

from apps.commands.infrastructure.admin import (
    CommandAdmin,
    CommandAttemptAdmin,
    DiscoverySessionAdmin,
)

__all__ = ["CommandAdmin", "CommandAttemptAdmin", "DiscoverySessionAdmin"]
