import os

INGESTION_BASE = os.getenv("INGESTION_BASE", "http://data_ingestion:8001")
MONITORING_BASE = os.getenv("MONITORING_BASE", "http://monitoring:8002")
EDGE_BASE = os.getenv("EDGE_BASE", "http://edge_controller:8003")
AI_BASE = os.getenv("AI_BASE", "http://ai_decision:8004")
TIMEOUT_SEC = float(os.getenv("INTEGRATIONS_TIMEOUT", "3"))
