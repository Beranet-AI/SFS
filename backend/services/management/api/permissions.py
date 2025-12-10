from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from django.conf import settings


class IsAuthenticatedOrService(BasePermission):
    """
    اجازه دسترسی به کاربران احراز هویت‌شده یا درخواست‌های سرویس با توکن معتبر.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        expected_token = getattr(settings, "DJANGO_SERVICE_TOKEN", None)
        auth_header = request.headers.get("Authorization", "")
        return bool(request.user and request.user.is_authenticated) or (
            expected_token and auth_header == f"Token {expected_token}"
        )
