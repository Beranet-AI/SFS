from apps.farms.domain.entities.farm import Farm

class CreateFarmUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, id: str, name: str) -> Farm:
        return self.repo.create(Farm(id=id, name=name))
