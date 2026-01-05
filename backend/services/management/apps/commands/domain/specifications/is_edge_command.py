from apps.commands.domain.repositories.capability_repository import CapabilityRepository


class IsEdgeCommand:
    def __init__(self, *, capability_repository: CapabilityRepository) -> None:
        self._capability_repository = capability_repository

    def __call__(
        self,
        *,
        device_category: str | None,
        device_type: str | None,
        command_type: str,
    ) -> bool:
        if device_type == "edge_controller":
            return True

        for capability in self._capability_repository.list_capabilities():
            if (
                capability.command_type == command_type
                and capability.device_type == "edge_controller"
            ):
                if device_category and capability.device_category != device_category:
                    continue
                if device_type and capability.device_type != device_type:
                    continue
                return True
        return False
