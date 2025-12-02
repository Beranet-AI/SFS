from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DJANGO_API_BASE_URL: str = "http://smartfarm_django:8000/api/v1"
    DJANGO_SERVICE_TOKEN: str = "super-secret-token"

    class Config:
        env_file = ".env.docker"

settings = Settings()
