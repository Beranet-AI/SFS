import logging
from pathlib import Path

from pydantic_settings import BaseSettings


logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    django_api_base_url: str
    django_service_token: str

    class Config:
        env_file = ".env.docker"

settings = Settings()
_env_file_path = Path(Settings.Config.env_file)
logger.info(
    "Loaded FastAPI settings from env_file=%s (exists=%s) with DJANGO_API_BASE_URL=%s",
    _env_file_path.resolve(),
    _env_file_path.exists(),
    settings.django_api_base_url,
)
