"""Domain layer root package.

Imports are re-exported from :mod:`backend.domain.entities` to provide a
stable API for services that rely on shared domain contracts.
"""

from . import entities
from .entities import *  # noqa: F401,F403

__all__ = entities.__all__
