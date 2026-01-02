# farm/infrastructure/mappers.py
from ..domain.entities.farm import Farm
from ..domain.entities.barn import Barn
from ..domain.entities.zone import Zone
from ..domain.value_objects.location import Location
from ..domain.value_objects.environmental_metrics import EnvironmentalMetrics
from ..domain.value_objects.economic_metrics import EconomicMetrics
from .models.models import FarmModel, BarnModel, ZoneModel


class FarmMapper:

    # ---------- ORM → Domain ----------

    @staticmethod
    def to_domain(model: FarmModel) -> Farm:
        location = Location(
            country=model.country,
            city=model.city,
            latitude=model.latitude or 0.0,
            longitude=model.longitude or 0.0,
        )

        farm = Farm(
            farm_id=str(model.id),
            name=model.name,
            location=location,
        )

        # Economic snapshot
        if model.feed_cost is not None:
            farm.economic = EconomicMetrics(
                feed_cost=model.feed_cost or 0.0,
                treatment_cost=model.treatment_cost or 0.0,
                revenue=model.revenue or 0.0,
            )

        # Barns + Zones
        for barn_model in model.barns.all():
            barn = Barn(
                barn_id=str(barn_model.id),
                name=barn_model.name,
            )

            for zone_model in barn_model.zones.all():
                zone = Zone(
                    zone_id=str(zone_model.id),
                    name=zone_model.name,
                )

                if zone_model.temperature_c is not None:
                    zone.environment = EnvironmentalMetrics(
                        temperature_c=zone_model.temperature_c,
                        humidity=zone_model.humidity or 0.0,
                        ammonia_ppm=zone_model.ammonia_ppm or 0.0,
                        co2_ppm=zone_model.co2_ppm,
                        airflow_mps=zone_model.airflow_mps,
                    )

                barn.zones.append(zone)

            farm.barns.append(barn)

        return farm
