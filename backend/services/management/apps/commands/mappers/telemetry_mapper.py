class InboundTelemetryMapper:
    @staticmethod
    def from_payload(payload: dict) -> dict:
        return dict(payload)
