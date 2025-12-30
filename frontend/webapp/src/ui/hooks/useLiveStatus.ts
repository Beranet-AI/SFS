"use client";

import { useEffect, useRef, useState } from "react";
import {
  fetchLiveStatusRecent,
  openLiveStatusStream,
} from "@/infrastructure/http/monitoringApi";
import { mapLiveStatus } from "@/domain/mappers/livestatusMapper";
import type { LiveStatus } from "@/domain/models/LiveStatus";
import { seedLiveStatus } from "@/domain/seed/dashboardSeed";
import type { DataSource } from "@/ui/types/DataSource";

type UseLiveStatusOptions = {
  useSeed?: boolean;
};

export function useLiveStatus(
  livestockId?: string,
  options: UseLiveStatusOptions = {}
) {
  const [data, setData] = useState<LiveStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [source, setSource] = useState<DataSource>("live");
  const esRef = useRef<EventSource | null>(null);
  const { useSeed } = options;

  useEffect(() => {
    let alive = true;

    // اگر livestockId نداریم، فقط loading را خاموش کن
    if (!livestockId) {
      setLoading(false);
      return;
    }

    if (useSeed) {
      setData(seedLiveStatus.filter((item) => item.livestockId === livestockId));
      setSource("seed");
      setLoading(false);
      return;
    }

    // 1) initial snapshot
    fetchLiveStatusRecent(livestockId)
      .then((rows) => {
        if (!alive) return;
        const mapped = rows.map(mapLiveStatus);
        if (mapped.length === 0) {
          setData(
            seedLiveStatus.filter((item) => item.livestockId === livestockId)
          );
          setSource("seed");
        } else {
          setData(mapped);
          setSource("live");
        }
      })
      .catch(() => {
        if (!alive) return;
        setData(seedLiveStatus.filter((item) => item.livestockId === livestockId));
        setSource("seed");
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
      // EventSource auto-retries
    };

    return () => {
      alive = false;
      es.close();
      esRef.current = null;
    };
  }, [livestockId, useSeed]);

  return { data, loading, source };
}
