"""Backwards-compatibility shim for middleware imports.

Infrastructure middleware now lives under
:mod:`management.infrastructure.middleware`. This module re-exports the
classes so existing import paths keep working during the refactor.
"""

from management.infrastructure.middleware import AllowAllHostsMiddleware, ServiceTokenAuthMiddleware

__all__ = ["AllowAllHostsMiddleware", "ServiceTokenAuthMiddleware"]
