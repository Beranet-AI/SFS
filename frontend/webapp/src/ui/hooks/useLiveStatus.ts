"use client";

import { useEffect, useRef, useState } from "react";
import { fetchLiveStatusRecent, openLiveStatusStream } from "@/infrastructure/http/monitoringApi";
import { mapLiveStatus } from "@/domain/mappers/livestatusMapper";
import type { LiveStatus } from "@/domain/models/LiveStatus";

export function useLiveStatus(livestockId: string) {
  const [data, setData] = useState<LiveStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const esRef = useRef<EventSource | null>(null);

  useEffect(() => {
    let alive = true;

    // 1) initial snapshot
    fetchLiveStatusRecent(livestockId)
      .then((rows) => {
        if (!alive) return;
        setData(rows.map(mapLiveStatus));
      })
      .finally(() => {
        if (alive) setLoading(false);
      });

    // 2) realtime stream
    const es = openLiveStatusStream(livestockId);
    esRef.current = es;

    es.onmessage = (event) => {
      try {
        const raw = JSON.parse(event.data);
        const item = mapLiveStatus(raw);
        setData((prev) => {
          const next = [...prev, item];
          return next.slice(-200);
        });
      } catch {
        // ignore bad payload
      }
    };

    es.onerror = () => {
      // optional: close and let it reconnect by browser (EventSource does auto-retry)
      // or implement manual backoff if needed.
    };

    return () => {
      alive = false;
      es.close();
      esRef.current = null;
    };
  }, [livestockId]);

  return { data, loading };
}
