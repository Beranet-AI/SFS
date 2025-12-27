from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, extra="ignore")

    SERVICE_NAME: str = "monitoring"
    SERVICE_ENV: str = "dev"

    API_PREFIX: str = "/monitoring"

    # Heartbeat / offline detection
    HEARTBEAT_OFFLINE_THRESHOLD_SECONDS: int = 60
    HEARTBEAT_CHECK_INTERVAL_SECONDS: int = 10

    # SSE
    SSE_PING_INTERVAL_SECONDS: int = 15

    # External services (Docker network)
    MANAGEMENT_BASE_URL: str = "http://management:8000"
    EDGE_CONTROLLER_BASE_URL: str = "http://edge_controller:8003"


settings = Settings()
