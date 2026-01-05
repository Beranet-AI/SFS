from apps.commands.domain.repositories.capability_repository import CapabilityRepository


class SupportsCommands:
    def __init__(self, *, capability_repository: CapabilityRepository) -> None:
        self._capability_repository = capability_repository

    def categories_for(self, *, device_category: str, device_type: str) -> list[str]:
        categories: set[str] = set()
        for capability in self._capability_repository.list_capabilities():
            if (
                capability.device_category == device_category
                and capability.device_type == device_type
            ):
                categories.add(capability.command_category)
        return sorted(categories)
