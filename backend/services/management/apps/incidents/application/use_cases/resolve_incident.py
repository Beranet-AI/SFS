from datetime import datetime

class ResolveIncidentUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, incident_id):
        incident = self.repo.get_by_id(incident_id)
        incident.resolve(datetime.utcnow())
        self.repo.save(incident)
        return incident
