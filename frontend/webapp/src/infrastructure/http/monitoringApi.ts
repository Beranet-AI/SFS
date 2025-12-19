import { http } from "./httpClient";
import type { LiveStatusDTO } from "@/shared/dto";

const BASE = process.env.NEXT_PUBLIC_MONITORING_API!;

export function fetchLiveStatus(livestockId: string) {
  return http<LiveStatusDTO[]>(`${BASE}/api/v1/livestatus/${livestockId}`);
}
