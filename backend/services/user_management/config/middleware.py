from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import JsonResponse


class ServiceTokenAuthMiddleware(MiddlewareMixin):
    """
    Middleware برای بررسی توکن سرویس بین FastAPI و Django.
    این middleware فقط روی مسیرهایی که نیاز به احراز هویت بین‌سرویسی دارند اعمال می‌شود.
    """
    def process_request(self, request):
        # اگر توکنی تعریف نشده باشد، middleware کاری نمی‌کند
        expected_token = getattr(settings, 'SERVICE_TOKEN', None)
        if not expected_token:
            return None

        # گرفتن توکن از header
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
