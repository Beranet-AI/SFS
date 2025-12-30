"use client";

import { useEffect, useState } from "react";
import {
  fetchIncidents,
  ackIncident,
  resolveIncident,
} from "@/infrastructure/http/managementApi";
import { mapIncident } from "@/domain/mappers/incidentMapper";
import type { Incident } from "@/domain/models/Incident";
import { seedIncidents } from "@/domain/seed/dashboardSeed";
import type { DataSource } from "@/ui/types/DataSource";

type UseIncidentsOptions = {
  useSeed?: boolean;
};

export function useIncidents(options: UseIncidentsOptions = {}) {
  const [data, setData] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(true);
  const [source, setSource] = useState<DataSource>("live");

  const { useSeed } = options;

  const refresh = async () => {
    if (useSeed) {
      setData(seedIncidents);
      setSource("seed");
      return;
    }
    const rows = await fetchIncidents();
    const mapped = rows.map(mapIncident);
    if (mapped.length === 0) {
      setData(seedIncidents);
      setSource("seed");
    } else {
      setData(mapped);
      setSource("live");
    }
  };

  useEffect(() => {
    let active = true;
    refresh()
      .catch(() => {
        if (!active) return;
        setData(seedIncidents);
        setSource("seed");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [useSeed]);

  async function ack(id: string) {
    if (source === "seed") return;
    await ackIncident(id);
    await refresh();
  }

  async function resolve(id: string) {
    if (source === "seed") return;
    await resolveIncident(id);
    await refresh();
  }

  return { data, loading, ack, resolve, refresh, source };
}
