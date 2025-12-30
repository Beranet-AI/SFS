"use client";

import { useEffect, useState } from "react";
import type { HealthRisk } from "@/domain/models/HealthRisk";
import { seedHealthRisks } from "@/domain/seed/dashboardSeed";
import type { DataSource } from "@/ui/types/DataSource";

type UseHealthRisksOptions = {
  useSeed?: boolean;
};

export function useHealthRisks(options: UseHealthRisksOptions = {}) {
  const [data, setData] = useState<HealthRisk[]>([]);
  const [loading, setLoading] = useState(true);
  const [source, setSource] = useState<DataSource>("seed");
  const { useSeed } = options;

  useEffect(() => {
    setLoading(true);
    if (useSeed) {
      setData(seedHealthRisks);
      setSource("seed");
      setLoading(false);
      return;
    }

    // TODO: Replace seedHealthRisks with AI decision API once health risk endpoint is available.
    setData(seedHealthRisks);
    setSource("seed");
    setLoading(false);
  }, [useSeed]);

  return { data, loading, source };
}
