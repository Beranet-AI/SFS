# apps/farms/application/use_cases/register_zone/use_case.py

from ....domain.entities.zone import Zone
from .input_dto import RegisterZoneInputDTO
from .output_dto import RegisterZoneOutputDTO


class RegisterZoneUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, dto: RegisterZoneInputDTO) -> RegisterZoneOutputDTO:
        farm = self.repo.get_by_id(dto.farm_id)

        # پیدا کردن Barn (مالک Zone)
        barn = next(
            (b for b in farm.barns if b.id == dto.barn_id),
            None
        )
        if barn is None:
            raise ValueError("Barn not found")

        # ساخت Zone فقط از طریق Barn
        zone = Zone(
            zone_id=dto.zone_id,
            name=dto.name,
        )
        barn.add_zone(zone)

        # ذخیره Aggregate Root
        self.repo.save(farm)

        return RegisterZoneOutputDTO(
            farm_id=farm.id,
            barn_id=barn.id,
            zone_id=zone.id,
        )
