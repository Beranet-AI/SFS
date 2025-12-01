from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    django_api_base_url: str
    django_service_token: str

    class Config:
        env_file = ".env.docker"

settings = Settings()
