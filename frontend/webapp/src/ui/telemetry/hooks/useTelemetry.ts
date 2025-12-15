'use client'

import { useEffect, useMemo, useState } from 'react'

import { fetchTelemetry } from '@/infrastructure/http/telemetryApi'
import type { TelemetryReading } from '@/types/Telemetry.dto'

export function useTelemetry(): {
  series: TelemetryReading[]
  loading: boolean
} {
  const [data, setData] = useState<TelemetryReading[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let mounted = true

    async function load() {
      setLoading(true)
      try {
        const result = await fetchTelemetry()
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

  const series = useMemo(() => data, [data])

  return { series, loading }
}
