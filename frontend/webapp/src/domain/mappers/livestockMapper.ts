import type { LivestockDTO } from "@/shared/dto";
import { HealthState } from "@/shared/enums";
import type { Livestock } from "@/domain/models/Livestock";

export function mapLivestock(dto: LivestockDTO): Livestock {
  return {
    id: dto.id,
    tag: dto.tag,
    farmId: dto.farm_id,
    barn: dto.barn,
    zone: dto.zone,
    healthState: dto.health_state as HealthState,
    healthConfidence: dto.health_confidence,
    healthEvaluatedAt: dto.health_evaluated_at,
  };
}
