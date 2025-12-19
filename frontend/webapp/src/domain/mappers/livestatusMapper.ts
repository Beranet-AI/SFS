import type { LiveStatusDTO } from "@/shared/dto";
import type { LiveStatus } from "@/domain/models/LiveStatus";

export function mapLiveStatus(dto: LiveStatusDTO): LiveStatus {
  return {
    deviceId: dto.device_id,
    livestockId: dto.livestock_id,
    metric: dto.metric,
    value: dto.value,
    recordedAt: dto.recorded_at,
  };
}
