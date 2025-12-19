"use client";

import { useEffect, useState } from "react";
import { fetchLivestock } from "@/infrastructure/http/managementApi";
import { mapLivestock } from "@/domain/mappers/livestockMapper";
import type { Livestock } from "@/domain/models/Livestock";

export function useLivestock() {
  const [data, setData] = useState<Livestock[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLivestock()
      .then((rows) => setData(rows.map(mapLivestock)))
      .finally(() => setLoading(false));
  }, []);

  return { data, loading };
}
