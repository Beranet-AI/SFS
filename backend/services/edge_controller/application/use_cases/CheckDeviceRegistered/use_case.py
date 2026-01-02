from ....infrastructure.registry.edge_registry import EdgeRegistry
from .check_device_registered_input import CheckDeviceRegisteredInput
from .check_device_registered_output import CheckDeviceRegisteredOutput


class CheckDeviceRegisteredUseCase:
    def __init__(self, registry: EdgeRegistry | None = None) -> None:
        self._registry = registry or EdgeRegistry()

    def execute(
        self, input_dto: CheckDeviceRegisteredInput
    ) -> CheckDeviceRegisteredOutput:
        if self._registry.is_approved(input_dto.device_id):
            return CheckDeviceRegisteredOutput(is_registered=True)

        return CheckDeviceRegisteredOutput(
            is_registered=bool(input_dto.device_id)
        )
