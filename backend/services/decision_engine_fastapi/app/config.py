from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    تنظیمات FastAPI برای اتصال به Django
    این کلاس envها را از محیط (یا فایل .env.docker داخل کانتینر) می‌خواند.
    """

    model_config = SettingsConfigDict(
        env_file=".env.docker",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    django_api_base_url: str  # مثلا: http://django:8000/api/v1
    django_token_url: str     # مثلا: http://django:8000/api/v1/auth/token/
    django_auth_username: str
    django_auth_password: str

    class Config:
        env_prefix = ""         # اسم فیلدها مستقیم از env خوانده می‌شود
        case_sensitive = False  # حروف کوچک/بزرگ مهم نباشد


settings = Settings()
