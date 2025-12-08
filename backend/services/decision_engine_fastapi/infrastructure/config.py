from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any

from pydantic import AnyUrl, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Typed configuration for the decision engine service."""

    model_config = SettingsConfigDict(env_file=".env.docker", extra="ignore")

    django_api_base_url: AnyUrl = Field(..., alias="DJANGO_API_BASE_URL")
    django_service_token: SecretStr = Field(..., alias="DJANGO_SERVICE_TOKEN")
    django_auth_username: str = Field(
        "fastapi_service", alias="DJANGO_AUTH_USERNAME", min_length=1
    )

    @property
    def api_base_url(self) -> str:
        """Normalized base URL without trailing slash."""

        return str(self.django_api_base_url).rstrip("/")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    logger.info(
        "Loaded FastAPI settings from env_file=%s with DJANGO_API_BASE_URL=%s",
        settings.model_config.get("env_file"),
        settings.api_base_url,
    )
    return settings


settings = get_settings()