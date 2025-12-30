"use client";

import { useEffect, useState } from "react";
import type { TelemetrySeries } from "@/domain/models/Telemetry";
import { seedTelemetrySeries } from "@/domain/seed/dashboardSeed";
import type { DataSource } from "@/ui/types/DataSource";

type UseTelemetryOptions = {
  useSeed?: boolean;
};

export function useTelemetrySeries(options: UseTelemetryOptions = {}) {
  const [data, setData] = useState<TelemetrySeries[]>([]);
  const [loading, setLoading] = useState(true);
  const [source, setSource] = useState<DataSource>("seed");
  const { useSeed } = options;

  useEffect(() => {
    setLoading(true);
    if (useSeed) {
      setData(seedTelemetrySeries);
      setSource("seed");
      setLoading(false);
      return;
    }

    // TODO: Replace seedTelemetrySeries with real monitoring API once telemetry endpoint is available.
    setData(seedTelemetrySeries);
    setSource("seed");
    setLoading(false);
  }, [useSeed]);

  return { data, loading, source };
}
