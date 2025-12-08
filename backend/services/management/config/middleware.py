<<<<<<< HEAD
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import JsonResponse

class ServiceTokenAuthMiddleware(MiddlewareMixin):
    """Allow service-to-service token auth without blocking browser users.

    If a ``DJANGO_SERVICE_TOKEN`` is configured, requests that include an
    ``Authorization: Token <token>`` header must match it. Requests without the
    header (normal browser/API clients using DRF authentication) are allowed to
    continue. Admin and static routes bypass the check to keep the admin usable
    even when the service token is misconfigured.
    """

    def process_request(self, request):
        if request.method == "OPTIONS":
            return None

        if request.path.startswith("/admin/") or request.path.startswith("/static/"):
            return None

        expected_token = getattr(settings, "DJANGO_SERVICE_TOKEN", None)
        auth_header = request.headers.get("Authorization", "").strip()

        # If no service token is configured or no Authorization header is sent,
        # let normal DRF/session authentication handle the request.
        if not expected_token or not auth_header:
            return None

        if auth_header.startswith("Token "):
            token = auth_header.removeprefix("Token ").strip()
            if token != expected_token:
                return JsonResponse({"detail": "Invalid service token"}, status=403)
        # Any other auth scheme should be handled by downstream authentication
        # classes, so we simply return None.
        return None

class AllowAllHostsMiddleware(MiddlewareMixin):
    """
    Middleware ساده برای اطمینان از اینکه HOST های ورودی رد نشوند.
    فقط در صورت نیاز خاص استفاده شود؛ در حالت معمولی ALLOWED_HOSTS کفایت می‌کند.
    """
    def process_request(self, request):
        return None
=======
"""Backwards-compatibility shim for middleware imports.

Infrastructure middleware now lives under
:mod:`management.infrastructure.middleware`. This module re-exports the
classes so existing import paths keep working during the refactor.
"""

from management.infrastructure.middleware import AllowAllHostsMiddleware, ServiceTokenAuthMiddleware

__all__ = ["AllowAllHostsMiddleware", "ServiceTokenAuthMiddleware"]
>>>>>>> e928450c31f6a2715453db0e3b4a646b6778af82
