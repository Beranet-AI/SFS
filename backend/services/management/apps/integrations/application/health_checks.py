from apps.integrations.infrastructure.clients.ingestion_client import IngestionClient
from apps.integrations.infrastructure.clients.monitoring_client import MonitoringClient
from apps.integrations.infrastructure.clients.edge_client import EdgeClient
from apps.integrations.infrastructure.clients.ai_client import AIClient

class HealthChecks:
    def __init__(self):
        self.ingestion = IngestionClient()
        self.monitoring = MonitoringClient()
        self.edge = EdgeClient()
        self.ai = AIClient()

    def check_all(self) -> dict:
        return {
            "ingestion": self.ingestion.ping(),
            "monitoring": self.monitoring.ping(),
            "edge": self.edge.ping(),
            "ai": self.ai.ping(),
        }
