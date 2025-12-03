import os
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class ServiceTokenAuthMiddleware:
    """
    احراز هویت بر اساس توکن ثابت بین سرویس‌ها (مثلاً FastAPI → Django).
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.expected_token = getattr(settings, "SERVICE_AUTH_TOKEN", None)
        self.service_username = os.getenv("DJANGO_AUTH_USERNAME")
        self.user_model = get_user_model()

    def __call__(self, request):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Token ", "")
        if request.path.startswith("/api/v1/") and self.expected_token:
            if token != self.expected_token:
                return JsonResponse({"detail": "Invalid or missing service token."}, status=401)
            if not self.service_username:
                return JsonResponse({"detail": "Service user not configured."}, status=401)

            try:
                request.user = self.user_model.objects.get(username=self.service_username)
                request._force_auth_user = request.user
            except self.user_model.DoesNotExist:
                logger.error(
                    "Service token validated but service user '%s' is missing. Run manage.py ensure_service_user.",
                    self.service_username,
                )
                return JsonResponse({"detail": "Service user missing."}, status=401)
        return self.get_response(request)
