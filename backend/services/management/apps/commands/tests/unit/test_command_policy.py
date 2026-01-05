from apps.commands.domain.domain_services.command_policy import CommandPolicy
from apps.commands.domain.repositories.capability_repository import (
    CapabilityRepository,
    CommandCapability,
)


class FakeCapabilityRepository(CapabilityRepository):
    def __init__(self, capabilities):
        self._capabilities = capabilities

    def list_capabilities(self):
        return list(self._capabilities)


def test_command_policy_defaults_and_adapter():
    repo = FakeCapabilityRepository(
        [
            CommandCapability(
                device_category="Infrastructure",
                device_type="edge_controller",
                command_category="Query",
                command_type="get_connected_devices",
                adapter_type="mqtt_json_v1",
            )
        ]
    )
    policy = CommandPolicy(capability_repository=repo)

    data = policy.apply(
        command_name="get_connected_devices",
        target_kind="location",
        target_id="edge-1",
        edge_node_id="edge-1",
        payload={"scan_id": "scan-1"},
        idempotency_key=None,
        ack_deadline_sec=None,
        result_deadline_sec=None,
        max_attempts=None,
        command_type="get_connected_devices",
        device_category="Infrastructure",
        device_type="edge_controller",
    )

    assert data["ack_deadline_sec"] == 10
    assert data["result_deadline_sec"] == 60
    assert data["max_attempts"] == 5
    assert data["payload"]["adapter_type"] == "mqtt_json_v1"
