from django.http import JsonResponse
from django.conf import settings

class ServiceTokenAuthMiddleware:
    """
    احراز هویت بر اساس توکن ثابت بین سرویس‌ها (مثلاً FastAPI → Django).
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.expected_token = getattr(settings, "SERVICE_AUTH_TOKEN", None)

    def __call__(self, request):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Token ", "")
        if request.path.startswith("/api/v1/") and self.expected_token:
            if token != self.expected_token:
                return JsonResponse({"detail": "Invalid or missing service token."}, status=401)
        return self.get_response(request)
