class ForwardService:
    """
    Forwards telemetry payloads from edge -> data_ingestion.
    """

    def __init__(self, ingestion_client):
        self.ingestion_client = ingestion_client

    def forward_telemetry(self, payload: dict):
        self.ingestion_client.push_telemetry(payload)
        return {"ok": True}
