from pydantic import BaseModel
import os


class Settings(BaseModel):
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "data_ingestion")
    SERVICE_ENV: str = os.getenv("SERVICE_ENV", "dev")

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8001"))

    MANAGEMENT_BASE_URL: str = os.getenv("MANAGEMENT_BASE_URL", "http://management:8000")
    MONITORING_BASE_URL: str = os.getenv("MONITORING_BASE_URL", "http://monitoring:8002")
    AI_DECISION_BASE_URL: str = os.getenv("AI_DECISION_BASE_URL", "http://ai_decision:8004")

    ENABLE_RULE_DISPATCH: bool = os.getenv("ENABLE_RULE_DISPATCH", "1") == "1"
    ENABLE_LIVESTATUS_PUSH: bool = os.getenv("ENABLE_LIVESTATUS_PUSH", "1") == "1"


settings = Settings()
