"use client";

import { useEffect, useState } from "react";
import { fetchLiveStatus } from "@/infrastructure/http/monitoringApi";
import { mapLiveStatus } from "@/domain/mappers/livestatusMapper";
import type { LiveStatus } from "@/domain/models/LiveStatus";

export function useLiveStatus(livestockId: string) {
  const [data, setData] = useState<LiveStatus[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLiveStatus(livestockId)
      .then((rows) => setData(rows.map(mapLiveStatus)))
      .finally(() => setLoading(false));
  }, [livestockId]);

  return { data, loading };
}
