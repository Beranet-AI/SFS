from pydantic import BaseModel
import os

class Settings(BaseModel):
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "monitoring")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8002"))

    ENABLE_SSE: bool = os.getenv("ENABLE_SSE", "true").lower() == "true"
    SSE_HEARTBEAT_SECONDS: int = int(os.getenv("SSE_HEARTBEAT_SECONDS", "10"))

settings = Settings()
