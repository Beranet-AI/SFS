"use client";

import { useEffect, useState } from "react";
import { fetchLivestock } from "@/infrastructure/http/managementApi";
import { mapLivestock } from "@/domain/mappers/livestockMapper";
import type { Livestock } from "@/domain/models/Livestock";
import { seedLivestock } from "@/domain/seed/dashboardSeed";
import type { DataSource } from "@/ui/types/DataSource";

type UseLivestockOptions = {
  useSeed?: boolean;
};

export function useLivestock(options: UseLivestockOptions = {}) {
  const [data, setData] = useState<Livestock[]>([]);
  const [loading, setLoading] = useState(true);
  const [source, setSource] = useState<DataSource>("live");

  const { useSeed } = options;

  useEffect(() => {
    let active = true;
    async function load() {
      setLoading(true);
      if (useSeed) {
        setData(seedLivestock);
        setSource("seed");
        setLoading(false);
        return;
      }
      try {
        const rows = await fetchLivestock();
        const mapped = rows.map(mapLivestock);
        if (!active) return;
        if (mapped.length === 0) {
          setData(seedLivestock);
          setSource("seed");
        } else {
          setData(mapped);
          setSource("live");
        }
      } catch {
        if (!active) return;
        setData(seedLivestock);
        setSource("seed");
      } finally {
        if (active) setLoading(false);
      }
    }
    load();
    return () => {
      active = false;
    };
  }, [useSeed]);

  return { data, loading, source };
}
