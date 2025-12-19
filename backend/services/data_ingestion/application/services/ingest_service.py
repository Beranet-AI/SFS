from data_ingestion.domain.telemetry_event import TelemetryEvent

class IngestService:
    """
    Coordinates telemetry ingestion.
    """

    def __init__(self, management_client, monitoring_client, rule_dispatcher):
        self.management_client = management_client
        self.monitoring_client = monitoring_client
        self.rule_dispatcher = rule_dispatcher

    def ingest(self, event: TelemetryEvent):
        # 1) persist raw telemetry (management / telemetry app)
        self.management_client.push_telemetry(event)

        # 2) update livestatus (monitoring)
        self.monitoring_client.push_livestatus(event)

        # 3) trigger rules
        self.rule_dispatcher.dispatch(event)
