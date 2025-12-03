import logging
from pathlib import Path

from pydantic_settings import BaseSettings


logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    DJANGO_API_BASE_URL: str = "http://smartfarm_django:8000/api/v1"
    DJANGO_SERVICE_TOKEN: str = "super-secret-token"
    DJANGO_AUTH_USERNAME: str = "fastapi_service"

    class Config:
        env_file = ".env.docker"

settings = Settings()

# 👇 این خط را اضافه کن
print("BASE URL =", settings.DJANGO_API_BASE_URL)

_env_file_path = Path(Settings.Config.env_file)
logger.info(
    "Loaded FastAPI settings from env_file=%s (exists=%s) with DJANGO_API_BASE_URL=%s",
    _env_file_path.resolve(),
    _env_file_path.exists(),
    settings.DJANGO_API_BASE_URL,
)