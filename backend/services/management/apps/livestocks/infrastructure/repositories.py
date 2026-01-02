# livestock/infrastructure/repositories.py
from django.db import transaction
from ..domain.repositories.livestock_repository import LivestockRepository
from .models.models import (
    LivestockModel,
    HealthRecordModel,
    MilkRecordModel,
    DiseaseRecordModel,
)
from .mappers import LivestockMapper


class LivestockRepositoryImpl(LivestockRepository):

    def get_by_id(self, livestock_id: str):
        model = (
            LivestockModel.objects
            .prefetch_related("disease_records")
            .get(id=livestock_id)
        )
        return LivestockMapper.to_domain(model)

    def save(self, livestock):
        with transaction.atomic():
            model, _ = LivestockModel.objects.update_or_create(
                id=livestock.id,
                defaults={
                    # Identity
                    "tag_id": livestock.identity.tag_id,
                    "breed": livestock.identity.breed,
                    "birth_date": livestock.identity.birth_date,
                    "sex": livestock.identity.sex,
                    "herd_entry_date": livestock.identity.herd_entry_date,
                    "status": livestock.identity.status,

                    # Health snapshot
                    "temperature_c": livestock.health.temperature_c if livestock.health else None,
                    "activity": livestock.health.activity if livestock.health else None,
                    "rumination_minutes": livestock.health.rumination_minutes if livestock.health else None,
                    "movement_index": livestock.health.movement_index if livestock.health else None,
                    "lying_minutes": livestock.health.lying_minutes if livestock.health else None,
                    "standing_minutes": livestock.health.standing_minutes if livestock.health else None,
                    "heart_rate_bpm": livestock.health.heart_rate_bpm if livestock.health else None,

                    # Nutrition snapshot
                    "feed_intake_kg": livestock.nutrition.feed_intake_kg if livestock.nutrition else None,
                    "water_intake_l": livestock.nutrition.water_intake_l if livestock.nutrition else None,
                    "feeder_station_id": livestock.nutrition.feeder_station_id if livestock.nutrition else None,

                    # Milk snapshot
                    "milk_volume_l": livestock.milk.volume_l if livestock.milk else None,
                    "milk_ec": livestock.milk.ec if livestock.milk else None,
                    "milk_temp_c": livestock.milk.milk_temp_c if livestock.milk else None,
                    "milk_scc": livestock.milk.scc if livestock.milk else None,

                    # Reproduction snapshot
                    "estrus": livestock.reproduction.estrus if livestock.reproduction else False,
                    "pregnant": livestock.reproduction.pregnant if livestock.reproduction else False,
                    "insemination_date": livestock.reproduction.insemination_date if livestock.reproduction else None,
                    "insemination_method": livestock.reproduction.insemination_method if livestock.reproduction else None,
                    "insemination_result": livestock.reproduction.insemination_result if livestock.reproduction else None,
                    "calving_date": livestock.reproduction.calving_date if livestock.reproduction else None,
                }
            )

            # Health history (append-only)
            if livestock.health:
                HealthRecordModel.objects.create(
                    livestock=model,
                    temperature_c=livestock.health.temperature_c,
                    activity=livestock.health.activity,
                    rumination_minutes=livestock.health.rumination_minutes,
                    movement_index=livestock.health.movement_index,
                    lying_minutes=livestock.health.lying_minutes,
                    standing_minutes=livestock.health.standing_minutes,
                    heart_rate_bpm=livestock.health.heart_rate_bpm,
                )

            # Milk history
            if livestock.milk:
                MilkRecordModel.objects.create(
                    livestock=model,
                    volume_l=livestock.milk.volume_l,
                    ec=livestock.milk.ec,
                    milk_temp_c=livestock.milk.milk_temp_c,
                    scc=livestock.milk.scc,
                )

            # Disease history (آخرین مورد)
            if livestock.diseases:
                d = livestock.diseases[-1]
                DiseaseRecordModel.objects.create(
                    livestock=model,
                    disease_name=d.disease_name,
                    diagnosed_at=d.diagnosed_at,
                    medication_name=d.medication_name,
                    milk_withdrawal_days=d.milk_withdrawal_days,
                )
