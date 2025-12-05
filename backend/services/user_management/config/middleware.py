from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import JsonResponse


class ServiceTokenAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # مسیرهایی که نیاز به توکن ندارند
        public_paths = ['/admin/', '/static/', '/media/', '/favicon.ico']

        if any(request.path.startswith(p) for p in public_paths):
            return None

        expected_token = getattr(settings, 'DJANGO_SERVICE_TOKEN', None)
        if not expected_token:
            return None

        print("Authorization header received:", request.headers.get("Authorization"))    #تست

        token = request.headers.get('Authorization', '').replace('Token ', '')

        if token != expected_token:
            return JsonResponse({'detail': 'Invalid service token'}, status=403)

        return None



class AllowAllHostsMiddleware(MiddlewareMixin):
    """
    Middleware ساده برای اطمینان از اینکه HOST های ورودی رد نشوند.
    فقط در صورت نیاز خاص استفاده شود؛ در حالت معمولی ALLOWED_HOSTS کفایت می‌کند.
    """
    def process_request(self, request):
        # این middleware کاری خاصی انجام نمی‌دهد مگر اینکه بخواهی رفتار خاصی لاگ کنی یا تغییر بدی.
        return None
