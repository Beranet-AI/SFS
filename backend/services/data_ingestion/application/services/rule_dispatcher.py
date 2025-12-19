class RuleDispatcher:
    """
    Dispatches telemetry to rule engine.
    """

    def __init__(self, rules_client):
        self.rules_client = rules_client

    def dispatch(self, event):
        self.rules_client.evaluate(event)
