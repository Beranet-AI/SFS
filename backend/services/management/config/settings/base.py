# config/settings.py
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# Add the services root (backend/services) to PYTHONPATH so shared apps like
# monitoring can be imported even when they live outside the Django project
sys.path.append(str(BASE_DIR.parent))

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() == "true"


def _split_env_list(var_name: str, default: str):
    return [host.strip() for host in os.getenv(var_name, default).split(",") if host.strip()]


ALLOWED_HOSTS = _split_env_list(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,django,fastapi,smartfarm-django,smartfarm-django:8000",
)

if DEBUG:
    ALLOWED_HOSTS += ["*"]

USE_X_FORWARDED_HOST = True

'''
   INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "api",
    "farm",
    "devices",
    "telemetry",
    "livestock",
    "health",
    "alerts",
]
'''
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",

    # Local apps
    "apps.incidents.apps.IncidentsConfig",
    "apps.monitoring.apps.MonitoringConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # ← باید بالاترین باشد
    "management.infrastructure.middleware.ServiceTokenAuthMiddleware",
    "management.infrastructure.middleware.AllowAllHostsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

_use_postgres_env = os.getenv("USE_POSTGRES")
USE_POSTGRES = (
    (_use_postgres_env.lower() == "true")
    if _use_postgres_env is not None
    else bool(os.getenv("DATABASE_URL") or os.getenv("POSTGRES_HOST"))
)

if USE_POSTGRES:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "smartfarm"),
            "USER": os.getenv("POSTGRES_USER", "smartfarm"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "smartfarm_password"),
            "HOST": os.getenv("POSTGRES_HOST", "db"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

CORS_ALLOWED_ORIGINS = _split_env_list(
    "DJANGO_CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:9000,http://fastapi:9000",
)
CORS_ALLOW_CREDENTIALS = True

DJANGO_SERVICE_TOKEN = os.getenv("DJANGO_SERVICE_TOKEN")

if DEBUG:
    print("Effective ALLOWED_HOSTS =", ALLOWED_HOSTS)
