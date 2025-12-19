import { http } from "./httpClient";
import type { LivestockDTO, IncidentDTO } from "@/shared/dto";

const BASE = process.env.NEXT_PUBLIC_MANAGEMENT_API!;

export function fetchLivestock() {
  return http<LivestockDTO[]>(`${BASE}/api/v1/livestock/`);
}

export function fetchIncidents() {
  return http<IncidentDTO[]>(`${BASE}/api/v1/incidents/`);
}

export function ackIncident(id: string) {
  return http<{ id: string; status: string }>(
    `${BASE}/api/v1/incidents/${id}/ack/`,
    { method: "POST" }
  );
}

export function resolveIncident(id: string) {
  return http<{ id: string; status: string }>(
    `${BASE}/api/v1/incidents/${id}/resolve/`,
    { method: "POST" }
  );
}

export function evaluateLivestockHealth(livestockId: string, score: number) {
  return http(`${BASE}/api/v1/livestock/${livestockId}/evaluate-health/`, {
    method: "POST",
    body: JSON.stringify({ score }),
  });
}
