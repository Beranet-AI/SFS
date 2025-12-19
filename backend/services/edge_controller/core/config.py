import os

SERVICE_NAME = "edge_controller"

DATA_INGESTION_BASE = os.getenv(
    "DATA_INGESTION_BASE",
    "http://data_ingestion:8001",
)
