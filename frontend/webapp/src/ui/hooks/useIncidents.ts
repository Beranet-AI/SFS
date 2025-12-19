"use client";

import { useEffect, useState } from "react";
import { fetchIncidents, ackIncident, resolveIncident } from "@/infrastructure/http/managementApi";
import { mapIncident } from "@/domain/mappers/incidentMapper";
import type { Incident } from "@/domain/models/Incident";

export function useIncidents() {
  const [data, setData] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = () =>
    fetchIncidents().then((rows) => setData(rows.map(mapIncident)));

  useEffect(() => {
    refresh().finally(() => setLoading(false));
  }, []);

  async function ack(id: string) {
    await ackIncident(id);
    await refresh();
  }

  async function resolve(id: string) {
    await resolveIncident(id);
    await refresh();
  }

  return { data, loading, ack, resolve, refresh };
}
