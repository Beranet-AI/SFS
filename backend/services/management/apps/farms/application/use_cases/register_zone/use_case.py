# farm/application/use_cases/register_zone/use_case.py
from ....domain.entities.zone import Zone

class RegisterZoneUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, dto):
        farm = self.repo.get_by_id(dto.farm_id)
        farm.add_zone(dto.barn_id, Zone(dto.zone_id, dto.name))
        self.repo.save(farm)
        return {"zone_id": dto.zone_id}
