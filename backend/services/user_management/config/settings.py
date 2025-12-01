import os
from datetime import timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

# --- تنظیمات عمومی با ENV (برای dev و docker) ---
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key-change-me")

DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() == "true"


def _split_env_list(var_name: str, default: str):
    return [host.strip() for host in os.getenv(var_name, default).split(",") if host.strip()]


ALLOWED_HOSTS = _split_env_list(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,django,fastapi",
)

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
    "alerts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "api.middleware.ServiceTokenAuthMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"



# آیا از PostgreSQL استفاده کنیم؟ (در Docker این مقدار true است)
USE_POSTGRES = os.getenv("USE_POSTGRES", "false").lower() == "true"

if USE_POSTGRES:
    required_pg_envs = ["POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT"]
    missing = [var for var in required_pg_envs if not os.getenv(var)]
    if missing:
        raise RuntimeError(
            f"USE_POSTGRES is true but required database environment variables are missing: {', '.join(missing)}"
        )
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "smartfarm"),
            "USER": os.getenv("POSTGRES_USER", "smartfarm"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "smartfarm_password"),
            "HOST": os.getenv("POSTGRES_HOST", "db"),      # اسم سرویس در docker-compose
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
else:
    # حالت توسعه محلی (بدون Docker) – همینی که قبلاً داشتی
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
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

CORS_ALLOWED_ORIGINS = _split_env_list(
    "DJANGO_CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:9000,http://fastapi:9000",
)
CORS_ALLOW_CREDENTIALS = True

SERVICE_AUTH_TOKEN = os.getenv("SERVICE_AUTH_TOKEN", "super-secret-token")
