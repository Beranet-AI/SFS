# File: livestock/domain/entities/livestock.py
from typing import Optional, List
from ..value_objects.identity import Identity
from ..value_objects.health_metrics import HealthMetrics
from ..value_objects.nutrition_metrics import NutritionMetrics
from ..value_objects.milk_production import MilkProduction
from ..value_objects.reproduction import ReproductionStatus
from ..value_objects.disease_record import DiseaseRecord
from ..domain_events.livestock_created import LivestockCreated
from ..domain_events.health_anomaly_detected import HealthAnomalyDetected
from ..domain_events.estrus_detected import EstrusDetected
from ..domain_events.disease_diagnosed import DiseaseDiagnosed
from ..domain_events.treatment_completed import TreatmentCompleted

class Livestock:
    """
    Aggregate Root
    """
    def __init__(self, livestock_id: str, identity: Identity):
        self.id = livestock_id
        self.identity = identity

        self.health: Optional[HealthMetrics] = None
        self.nutrition: Optional[NutritionMetrics] = None
        self.milk: Optional[MilkProduction] = None
        self.reproduction: Optional[ReproductionStatus] = None
        self.diseases: List[DiseaseRecord] = []

        self._events: List[object] = []

    @staticmethod
    def create(livestock_id: str, identity: Identity) -> "Livestock":
        obj = Livestock(livestock_id, identity)
        obj._events.append(LivestockCreated(livestock_id))
        return obj

    def record_health_metrics(self, metrics: HealthMetrics):
        self.health = metrics
        if metrics.temperature_c >= 39.0:
            self._events.append(HealthAnomalyDetected(self.id, metrics.temperature_c))

    def record_nutrition_metrics(self, metrics: NutritionMetrics):
        self.nutrition = metrics

    def record_milk_production(self, metrics: MilkProduction):
        self.milk = metrics

    def record_reproduction_status(self, status: ReproductionStatus):
        self.reproduction = status
        if status.estrus and not status.pregnant:
            self._events.append(EstrusDetected(self.id))

    def diagnose_disease(self, record: DiseaseRecord):
        self.diseases.append(record)
        self._events.append(DiseaseDiagnosed(self.id, record.disease_name))

    def complete_treatment(self, medication_name: str):
        self._events.append(TreatmentCompleted(self.id, medication_name))

    def pull_events(self):
        events = self._events[:]
        self._events.clear()
        return events
