import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "monitoring"
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "smartfarm-services")


settings = Settings()
