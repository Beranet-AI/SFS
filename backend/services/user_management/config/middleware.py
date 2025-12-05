from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import JsonResponse

class ServiceTokenAuthMiddleware(MiddlewareMixin):
    """
    Middleware برای بررسی توکن سرویس بین FastAPI و Django.
    این middleware فقط روی مسیرهایی که نیاز به احراز هویت بین‌سرویسی دارند اعمال می‌شود.
    
    def process_request(self, request):
        # عبور درخواست‌های OPTIONS بدون بررسی توکن (برای CORS preflight)
        if request.method == 'OPTIONS':
            return None

        expected_token = getattr(settings, 'DJANGO_SERVICE_TOKEN', None)
        if not expected_token:
            return None

        token = request.headers.get('Authorization', '').replace('Token ', '')

        if token != expected_token:
            return JsonResponse({'detail': 'Invalid service token'}, status=403)

        return None
    """
    def process_request(self, request):
    # اجازه دسترسی به /admin/ و static files
         if request.path.startswith("/admin/") or request.path.startswith("/static/"):
             return None

         expected_token = getattr(settings, 'DJANGO_SERVICE_TOKEN', None)
   
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
        return None
