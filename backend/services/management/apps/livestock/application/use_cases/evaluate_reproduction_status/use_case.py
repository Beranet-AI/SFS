# File: livestock/application/use_cases/evaluate_reproduction_status/use_case.py
from ....domain.value_objects.reproduction import ReproductionStatus

class EvaluateReproductionStatusUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, input_dto):
        livestock = self.repo.get_by_id(input_dto.livestock_id)
        status = ReproductionStatus(
            estrus=input_dto.estrus,
            pregnant=input_dto.pregnant,
            insemination_date=input_dto.insemination_date,
            insemination_method=input_dto.insemination_method,
            insemination_result=input_dto.insemination_result,
            calving_date=input_dto.calving_date,
        )
        livestock.record_reproduction_status(status)
        self.repo.save(livestock)
        events = [e.__class__.__name__ for e in livestock.pull_events()]
        return {"livestock_id": livestock.id, "events": events}
