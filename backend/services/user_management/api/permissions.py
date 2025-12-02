# api/permissions.py

from rest_framework.permissions import BasePermission

class IsAuthenticatedOrService(BasePermission):
    """
    اجازه دسترسی به کاربران لاگین‌شده یا درخواست‌هایی که توسط سرویس تأیید شده‌اند (service_authenticated).
    """
    def has_permission(self, request, view):
        return (
            bool(request.user and request.user.is_authenticated)
            or getattr(request, "service_authenticated", False)
        )
