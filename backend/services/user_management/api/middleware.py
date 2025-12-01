from django.conf import settings
from django.http import JsonResponse

class ServiceTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.token = settings.SERVICE_TOKEN

    def __call__(self, request):
        auth_header = request.headers.get("Authorization", "")
        prefix = "Token "

        if auth_header.startswith(prefix):
            token = auth_header[len(prefix):]
            if token == self.token:
                request.service_authenticated = True
            else:
                return JsonResponse({"detail": "Invalid or missing service token."}, status=401)
        else:
            request.service_authenticated = False

        return self.get_response(request)
