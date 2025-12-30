"use client";

import { useEffect, useState } from "react";
import type { Farm } from "@/domain/models/Farm";
import { seedFarms } from "@/domain/seed/dashboardSeed";
import type { DataSource } from "@/ui/types/DataSource";
import { fetchFarms } from "@/infrastructure/http/managementApi";

type UseFarmsOptions = {
  useSeed?: boolean;
};

export function useFarms(options: UseFarmsOptions = {}) {
  const [data, setData] = useState<Farm[]>([]);
  const [source, setSource] = useState<DataSource>("seed");
  const { useSeed } = options;

  useEffect(() => {
    let active = true;
    async function load() {
      if (useSeed) {
        setData(seedFarms);
        setSource("seed");
        return;
      }
      try {
        const farms = await fetchFarms();
        if (!active) return;
        if (farms.length === 0) {
          setData(seedFarms);
          setSource("seed");
        } else {
          setData(
            farms.map((farm) => ({
              id: String(farm.id),
              name: farm.name,
              // TODO: Populate location/status/livestockCount/devicesOnline once backend exposes fields.
              location: "—",
              status: "active",
              livestockCount: 0,
              devicesOnline: 0,
            }))
          );
          setSource("live");
        }
      } catch {
        if (!active) return;
        setData(seedFarms);
        setSource("seed");
      }
    }
    load();
    return () => {
      active = false;
    };
  }, [useSeed]);

  return { data, source };
}
