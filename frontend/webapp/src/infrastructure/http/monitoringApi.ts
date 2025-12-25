export const MONITORING_BASE_URL =
  process.env.NEXT_PUBLIC_MONITORING_BASE_URL ?? "http://localhost:8002";

export async function fetchLiveStatusRecent(livestockId: string) {
  const url = `${MONITORING_BASE_URL}/monitoring/livestatus/recent?livestock_id=${encodeURIComponent(
    livestockId
  )}`;
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch livestatus recent");
  return res.json();
}

export function openLiveStatusStream(livestockId: string) {
  const url = `${MONITORING_BASE_URL}/monitoring/livestatus/stream?livestock_id=${encodeURIComponent(
    livestockId
  )}`;
  return new EventSource(url);
}
