# farm/infrastructure/repositories.py
from django.db import transaction
from ..domain.repositories.farm_repository import FarmRepository
from ..domain.entities.farm import Farm
from ..domain.value_objects.environmental_metrics import EnvironmentalMetrics
from .models import (
    FarmModel,
    BarnModel,
    ZoneModel,
    ZoneEnvironmentHistoryModel,
)
from .mappers import FarmMapper


class FarmRepositoryImpl(FarmRepository):

    def get_by_id(self, farm_id: str) -> Farm:
        model = (
            FarmModel.objects
            .prefetch_related("barns__zones")
            .get(id=farm_id)
        )
        return FarmMapper.to_domain(model)

    def save(self, farm: Farm) -> None:
        with transaction.atomic():
            farm_model, _ = FarmModel.objects.update_or_create(
                id=farm.id,
                defaults={
                    "name": farm.name,
                    "country": farm.location.country,
                    "city": farm.location.city,
                    "latitude": farm.location.latitude,
                    "longitude": farm.location.longitude,
                    "feed_cost": farm.economic.feed_cost if farm.economic else None,
                    "treatment_cost": farm.economic.treatment_cost if farm.economic else None,
                    "revenue": farm.economic.revenue if farm.economic else None,
                },
            )

            # ---- Sync Barns ----
            existing_barns = {str(b.id): b for b in farm_model.barns.all()}
            domain_barns = {b.id: b for b in farm.barns}

            # delete removed barns
            for barn_id in set(existing_barns) - set(domain_barns):
                existing_barns[barn_id].delete()

            for barn_id, barn in domain_barns.items():
                barn_model, _ = BarnModel.objects.update_or_create(
                    id=barn_id,
                    farm=farm_model,
                    defaults={"name": barn.name},
                )

                # ---- Sync Zones ----
                existing_zones = {str(z.id): z for z in barn_model.zones.all()}
                domain_zones = {z.id: z for z in barn.zones}

                # delete removed zones
                for zone_id in set(existing_zones) - set(domain_zones):
                    existing_zones[zone_id].delete()

                for zone_id, zone in domain_zones.items():
                    zone_model, _ = ZoneModel.objects.update_or_create(
                        id=zone_id,
                        barn=barn_model,
                        defaults={
                            "name": zone.name,
                            "temperature_c": zone.environment.temperature_c if zone.environment else None,
                            "humidity": zone.environment.humidity if zone.environment else None,
                            "ammonia_ppm": zone.environment.ammonia_ppm if zone.environment else None,
                            "co2_ppm": zone.environment.co2_ppm if zone.environment else None,
                            "airflow_mps": zone.environment.airflow_mps if zone.environment else None,
                        },
                    )

                    # ---- Environment history (append-only) ----
                    if zone.environment:
                        ZoneEnvironmentHistoryModel.objects.create(
                            zone=zone_model,
                            temperature_c=zone.environment.temperature_c,
                            humidity=zone.environment.humidity,
                            ammonia_ppm=zone.environment.ammonia_ppm,
                            co2_ppm=zone.environment.co2_ppm,
                            airflow_mps=zone.environment.airflow_mps,
                        )
