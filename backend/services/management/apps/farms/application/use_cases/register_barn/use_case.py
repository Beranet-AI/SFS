# farm/application/use_cases/register_barn/use_case.py
from ....domain.entities.barn import Barn

class RegisterBarnUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, dto):
        farm = self.repo.get_by_id(dto.farm_id)
        farm.add_barn(Barn(dto.barn_id, dto.name))
        self.repo.save(farm)
        return {"barn_id": dto.barn_id}
