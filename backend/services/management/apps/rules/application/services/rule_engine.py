class RuleEngine:
    def __init__(self, management_client, command_client):
        self.mgmt = management_client
        self.command = command_client
        self.buffers = {}

    def evaluate(self, telemetry, rule):
        key = (telemetry["device_serial"], rule["metric"])

        if rule["window_sec"]:
            buf = self.buffers.setdefault(
                key, TimeWindowBuffer(rule["window_sec"])
            )
            buf.add(telemetry["ts"], telemetry["value"])
            values = buf.values()
        else:
            values = [telemetry["value"]]

        if any(v > rule["threshold"] for v in values):
            self.mgmt.create_incident({...})

            if rule["control"]["enabled"]:
                self.command.send(rule["control"]["command"])
