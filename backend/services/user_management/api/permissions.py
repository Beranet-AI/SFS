# api/permissions.py

#from rest_framework.permissions import BasePermission

#class IsAuthenticatedOrService(BasePermission):
#    """
#    اجازه دسترسی به کاربران لاگین‌شده یا درخواست‌هایی که توسط سرویس تأیید شده‌اند (service_authenticated).
#    """
#    def has_permission(self, request, view):
#        return (
#            bool(request.user and request.user.is_authenticated)
#            or getattr(request, "service_authenticated", False)
#       )


from rest_framework.permissions import BasePermission
from django.conf import settings

class IsAuthenticatedOrService(BasePermission):
    def has_permission(self, request, view):
        expected_token = getattr(settings, 'DJANGO_SERVICE_TOKEN', None)
        auth_header = request.headers.get('Authorization', '')
        return (
            request.user and request.user.is_authenticated
        ) or (
            expected_token and auth_header == f"Token {expected_token}"
        )
