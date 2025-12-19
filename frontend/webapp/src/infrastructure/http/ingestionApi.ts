import { http } from "./httpClient";

const BASE = process.env.NEXT_PUBLIC_INGESTION_API!;

export function ingestTelemetry(payload: {
  device_id: string;
  livestock_id: string;
  metric: string;
  value: number;
  recorded_at?: string;
}) {
  return http(`${BASE}/api/v1/telemetry/ingest/`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
