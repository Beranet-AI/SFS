from pydantic import BaseModel
import os


class Settings(BaseModel):
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "edge_controller")
    SERVICE_ENV: str = os.getenv("SERVICE_ENV", "dev")

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8003"))

    # feature toggles
    ENABLE_DEVICE_DISCOVERY: bool = os.getenv("ENABLE_DEVICE_DISCOVERY", "1") == "1"
    ENABLE_TELEMETRY_FORWARD: bool = os.getenv("ENABLE_TELEMETRY_FORWARD", "1") == "1"
    ENABLE_COMMANDS: bool = os.getenv("ENABLE_COMMANDS", "1") == "1"

    MANAGEMENT_BASE_URL: str = os.getenv("MANAGEMENT_BASE_URL", "http://management:8000")
    DATA_INGESTION_BASE_URL: str = os.getenv("DATA_INGESTION_BASE_URL", "http://data_ingestion:8001")

    # labview ingress
    LABVIEW_INGRESS_AUTH_TOKEN: str = os.getenv("LABVIEW_INGRESS_AUTH_TOKEN", "dev-token")


settings = Settings()
