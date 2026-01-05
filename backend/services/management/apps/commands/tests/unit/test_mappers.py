from datetime import datetime

from apps.commands.infrastructure.mappers.command_mapper import CommandMapper


class CommandModelStub:
    def __init__(self):
        self.id = "cmd-1"
        self.command_name = "get_connected_devices"
        self.target_kind = "location"
        self.target_id = "edge-1"
        self.edge_node_id = "edge-1"
        self.payload = {"scan_id": "scan-1"}
        self.idempotency_key = "scan-1"
        self.status = "pending"
        self.source = "manual"
        self.created_by = "tester"
        self.created_at = datetime(2024, 1, 1)
        self.ack_deadline_sec = 10
        self.result_deadline_sec = 60
        self.max_attempts = 5
        self.acked_at = None
        self.started_at = None
        self.finished_at = None
        self.last_error_code = ""
        self.last_error_message = ""
        self.last_result = {}


def test_command_mapper_to_domain():
    model = CommandModelStub()
    command = CommandMapper.to_domain(model)

    assert command.id == "cmd-1"
    assert command.command_name == "get_connected_devices"
    assert command.status.value == "pending"
