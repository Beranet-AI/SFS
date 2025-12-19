import { http } from "./httpClient";

const BASE = process.env.NEXT_PUBLIC_AI_DECISION_API!;

export function runHealthDecision(livestockId: string) {
  return http<{
    livestock_id: string;
    score: number;
    state: string;
    predicted_at: string;
  }>(`${BASE}/api/v1/decision/health`, {
    method: "POST",
    body: JSON.stringify({ livestock_id: livestockId }),
  });
}
