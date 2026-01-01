# farm/application/use_cases/register_farm/use_case.py
from ....domain.entities.farm import Farm
from ....domain.value_objects.location import Location

class RegisterFarmUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, dto):
        location = Location(
            country=dto.country,
            city=dto.city,
            latitude=dto.latitude,
            longitude=dto.longitude,
        )
        farm = Farm.create(dto.farm_id, dto.name, location)
        self.repo.save(farm)
        return {"farm_id": farm.id}
