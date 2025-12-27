from apps.farms.models import FarmModel


class FarmService:
    """
    Application service for Farm orchestration.
    """

    # -------- Queries --------

    def get_by_id(self, *, farm_id: int) -> FarmModel:
        return FarmModel.objects.get(id=farm_id)

    def list_all(self):
        return FarmModel.objects.all().order_by("name")

    # -------- Commands --------

    def create(self, *, name: str) -> FarmModel:
        return FarmModel.objects.create(name=name)

    def rename(self, *, farm_id: int, name: str) -> FarmModel:
        farm = self.get_by_id(farm_id=farm_id)
        farm.name = name
        farm.save(update_fields=["name"])
        return farm

    def delete(self, *, farm_id: int) -> None:
        farm = self.get_by_id(farm_id=farm_id)
        farm.delete()
