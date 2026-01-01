# File: livestock/application/use_cases/record_milk_production/use_case.py
from ....domain.value_objects.milk_production import MilkProduction

class RecordMilkProductionUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, input_dto):
        livestock = self.repo.get_by_id(input_dto.livestock_id)
        livestock.record_milk_production(MilkProduction(
            volume_l=input_dto.volume_l,
            ec=input_dto.ec,
            milk_temp_c=input_dto.milk_temp_c,
            scc=input_dto.scc,
        ))
        self.repo.save(livestock)
        return {"livestock_id": livestock.id}
