from apps.commands.domain.enums.adapter_type import AdapterType
from apps.commands.domain.enums.command_category import CommandCategory
from apps.commands.domain.enums.command_type import CommandType
from apps.commands.domain.enums.device_category import DeviceCategory
from apps.commands.domain.enums.device_type import DeviceType
from apps.commands.domain.repositories.capability_repository import CommandCapability
from apps.commands.domain.repositories.capability_repository import CapabilityRepository


class DjangoCapabilityRepository(CapabilityRepository):
    def list_capabilities(self) -> list[CommandCapability]:
        return [
            CommandCapability(
                device_category=DeviceCategory.INFRASTRUCTURE.value,
                device_type=DeviceType.EDGE_CONTROLLER.value,
                command_category=CommandCategory.QUERY.value,
                command_type=CommandType.GET_CONNECTED_DEVICES.value,
                adapter_type=AdapterType.MQTT_JSON_V1.value,
            ),
            CommandCapability(
                device_category=DeviceCategory.INFRASTRUCTURE.value,
                device_type=DeviceType.EDGE_CONTROLLER.value,
                command_category=CommandCategory.CONFIGURATION.value,
                command_type=CommandType.SET_NETWORK.value,
                adapter_type=AdapterType.MQTT_JSON_V1.value,
            ),
            CommandCapability(
                device_category=DeviceCategory.INFRASTRUCTURE.value,
                device_type=DeviceType.EDGE_CONTROLLER.value,
                command_category=CommandCategory.CONFIGURATION.value,
                command_type=CommandType.SET_PROTOCOL.value,
                adapter_type=AdapterType.MQTT_JSON_V1.value,
            ),
        ]
