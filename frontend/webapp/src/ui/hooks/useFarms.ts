"use client";

import { useEffect, useState } from "react";
import type { Farm } from "@/domain/models/Farm";
import { seedFarms } from "@/domain/seed/dashboardSeed";
import type { DataSource } from "@/ui/types/DataSource";

type UseFarmsOptions = {
  useSeed?: boolean;
};

export function useFarms(options: UseFarmsOptions = {}) {
  const [data, setData] = useState<Farm[]>([]);
  const [source, setSource] = useState<DataSource>("seed");
  const { useSeed } = options;

  useEffect(() => {
    if (useSeed) {
      setData(seedFarms);
      setSource("seed");
      return;
    }

    // TODO: Replace seedFarms with real management API once /farms endpoint is available.
    setData(seedFarms);
    setSource("seed");
  }, [useSeed]);

  return { data, source };
}
