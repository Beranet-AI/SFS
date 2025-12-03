# config/middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.core.exceptions import DisallowedHost




class AllowAllHostsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            # اینجا اگر هدر معتبر نبود، حذف پورت و ادامه
            request.get_host()
        except DisallowedHost:
            request.META["HTTP_HOST"] = request.META.get("HTTP_HOST", "").split(":")[0]


class ServiceTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.token = f"Token {settings.DJANGO_SERVICE_TOKEN}"

    def __call__(self, request):
        token = request.headers.get("Authorization")
        request.service_user_authenticated = token == self.token
        return self.get_response(request)
