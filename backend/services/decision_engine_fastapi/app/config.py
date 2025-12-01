from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DJANGO_API_BASE_URL: str
    DJANGO_SERVICE_TOKEN: str

    class Config:
        env_file = ".env.docker"

settings = Settings()
