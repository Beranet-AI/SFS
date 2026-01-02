# livestock/infrastructure/mappers.py
from ..domain.entities.livestock import Livestock
from ..domain.value_objects.identity import Identity
from ..domain.value_objects.health_metrics import HealthMetrics
from ..domain.value_objects.nutrition_metrics import NutritionMetrics
from ..domain.value_objects.milk_production import MilkProduction
from ..domain.value_objects.reproduction import ReproductionStatus
from ..domain.value_objects.disease_record import DiseaseRecord
from .models.models import LivestockModel


class LivestockMapper:

    @staticmethod
    def to_domain(model: LivestockModel) -> Livestock:
        identity = Identity(
            tag_id=model.tag_id,
            breed=model.breed,
            birth_date=model.birth_date,
            sex=model.sex,
            herd_entry_date=model.herd_entry_date,
            status=model.status,
        )

        livestock = Livestock(str(model.id), identity)

        # Health snapshot
        if model.temperature_c is not None:
            livestock.health = HealthMetrics(
                temperature_c=model.temperature_c,
                activity=model.activity or 0.0,
                rumination_minutes=model.rumination_minutes,
                movement_index=model.movement_index,
                lying_minutes=model.lying_minutes,
                standing_minutes=model.standing_minutes,
                heart_rate_bpm=model.heart_rate_bpm,
            )

        # Nutrition snapshot
        if model.feed_intake_kg is not None:
            livestock.nutrition = NutritionMetrics(
                feed_intake_kg=model.feed_intake_kg,
                water_intake_l=model.water_intake_l or 0.0,
                feeder_station_id=model.feeder_station_id,
            )

        # Milk snapshot
        if model.milk_volume_l is not None:
            livestock.milk = MilkProduction(
                volume_l=model.milk_volume_l,
                ec=model.milk_ec or 0.0,
                milk_temp_c=model.milk_temp_c,
                scc=model.milk_scc,
            )

        # Reproduction snapshot
        livestock.reproduction = ReproductionStatus(
            estrus=model.estrus,
            pregnant=model.pregnant,
            insemination_date=model.insemination_date,
            insemination_method=model.insemination_method,
            insemination_result=model.insemination_result,
            calving_date=model.calving_date,
        )

        # Disease history
        for d in model.disease_records.all():
            livestock.diseases.append(DiseaseRecord(
                disease_name=d.disease_name,
                diagnosed_at=d.diagnosed_at,
                medication_name=d.medication_name,
                milk_withdrawal_days=d.milk_withdrawal_days,
            ))

        return livestock
