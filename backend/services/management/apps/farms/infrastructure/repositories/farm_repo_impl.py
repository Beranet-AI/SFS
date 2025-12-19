from apps.farms.domain.entities.farm import Farm
from apps.farms.infrastructure.models.farm_model import FarmModel

class DjangoFarmRepository:
    def get_by_id(self, farm_id: str) -> Farm:
        obj = FarmModel.objects.get(id=farm_id)
        return Farm(id=str(obj.id), name=obj.name)

    def create(self, farm: Farm) -> Farm:
        obj = FarmModel.objects.create(name=farm.name)
        return Farm(id=str(obj.id), name=obj.name)
