from apps.commands.domain.repositories.capability_repository import (
    CapabilityRepository,
    CommandCapability,
)
from apps.commands.domain.specifications.is_edge_command import IsEdgeCommand


class FakeCapabilityRepository(CapabilityRepository):
    def __init__(self, capabilities):
        self._capabilities = capabilities

    def list_capabilities(self):
        return list(self._capabilities)


def test_is_edge_command_matches_registry():
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
    spec = IsEdgeCommand(capability_repository=repo)

    assert (
        spec(
            device_category="Infrastructure",
            device_type="edge_controller",
            command_type="get_connected_devices",
        )
        is True
    )
    assert (
        spec(
            device_category="Device",
            device_type="sensor",
            command_type="custom",
        )
        is False
    )
