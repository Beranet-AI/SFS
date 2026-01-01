# File: livestock/application/use_cases/register_livestock/use_case.py
from ....domain.entities.livestock import Livestock
from ....domain.value_objects.identity import Identity

class RegisterLivestockUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, input_dto):
        identity = Identity(
            tag_id=input_dto.tag_id,
            breed=input_dto.breed,
            birth_date=input_dto.birth_date,
            sex=input_dto.sex,
            herd_entry_date=input_dto.herd_entry_date,
            status=input_dto.status,
        )
        livestock = Livestock.create(input_dto.livestock_id, identity)
        self.repo.save(livestock)
        return {"livestock_id": livestock.id}
