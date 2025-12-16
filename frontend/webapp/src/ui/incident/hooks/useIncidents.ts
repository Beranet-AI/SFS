// src/ui/incident/hooks/useIncidents.ts
'use client';

import { useEffect, useState } from 'react';
import { incidentsApi } from '@/infrastructure/http/management/incidentsApi';
import { mapIncidentToVM } from '@/mappers/incident/incidentMapper';
import type { IncidentVM } from '@/view-models/incident/IncidentVM';

/**
 * Hook responsible for:
 * - fetching incidents from Management
 * - mapping DTO -> VM
 *
 * NO domain logic
 * NO cross-service data
 */
export function useIncidents() {
  const [incidents, setIncidents] = useState<IncidentVM[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function load() {
      try {
        setLoading(true);
        const dtos = await incidentsApi.list();
        if (!active) return;

        setIncidents(dtos.map(mapIncidentToVM));
      } catch (err: any) {
        if (!active) return;
        setError(err?.message ?? 'Failed to load incidents');
      } finally {
        if (active) setLoading(false);
      }
    }

    load();

    return () => {
      active = false;
    };
  }, []);

  return {
    incidents,
    loading,
    error,
  };
}
