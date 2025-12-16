// src/ui/incident/hooks/useIncidents.ts

'use client'

import { useEffect, useState } from 'react'
import { incidentsApi } from '@/infrastructure/http/management/incidentsApi'
import { mapIncidentToViewModel } from '@/mappers/incident/incidentMapper'
import type { IncidentVM } from '@/view-models/incident/IncidentVM'

export function useIncidents() {
  const [incidents, setIncidents] = useState<IncidentVM[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    incidentsApi
      .list()
      .then((data) => {
        setIncidents(data.map(mapIncidentToViewModel))
      })
      .catch((err) => {
        setError(err as Error)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  return {
    incidents,
    loading,
    error,
  }
}
