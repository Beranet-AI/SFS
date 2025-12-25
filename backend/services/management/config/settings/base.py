from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ======================
# Core
# ======================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = False

ALLOWED_HOSTS = ["*"]

# ======================
# Applications
# ======================
INSTALLED_APPS = [
    # --- Django core ---
    "django.contrib.contenttypes",
    "django.contrib.auth",

    # --- YOUR APPS (قبل از admin) ---
    "apps.users.apps.UsersConfig",

    # --- Django admin بعد از users ---
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # --- بقیه اپ‌ها ---
    "apps.devices",
    "apps.farms",
    "apps.livestock",
    "apps.health",
    "apps.incidents",
    "apps.telemetry",
]
# ======================
# Custom User Model
# ======================
AUTH_USER_MODEL = "users.UserModel"

# ======================
# Middleware
# ======================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ======================
# URLs / ASGI / WSGI
# ======================
ROOT_URLCONF = "config.urls"

ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

# ======================
# Database (Docker-safe)
# ======================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "sfs"),
        "USER": os.environ.get("POSTGRES_USER", "sfs"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "sfs"),
        "HOST": os.environ.get("POSTGRES_HOST", "postgres"),  # 🔴 این مهم است
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# ======================
# Templates
# ======================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# ======================
# Static / Media
# ======================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
