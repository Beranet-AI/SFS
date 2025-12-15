'use client'

import { useEffect, useMemo, useState } from 'react'

import { fetchIncidents } from '@/infrastructure/http/management/incidentsApi'
import { mapIncidentToVM } from '@/mappers/incident/incidentMapper'

import type { Incident } from '@/types/incidentDto'
import type { IncidentVM } from '@/view-models/incident/IncidentVM'

export function useIncidents(): {
  incidents: IncidentVM[]
  loading: boolean
} {
  const [data, setData] = useState<Incident[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let mounted = true

    async function load() {
      setLoading(true)
      try {
        const result = await fetchIncidents()
        if (mounted) {
          setData(result)
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    load()

    return () => {
      mounted = false
    }
  }, [])

  const incidents = useMemo(() => {
    return data.map(mapIncidentToVM)
  }, [data])

  return { incidents, loading }
}
