'use client'

import { useEffect, useMemo, useState } from 'react'

import { fetchEvents } from '@/infrastructure/http/eventsApi'
import { mapEventToVM } from '@/mappers/event/eventMapper'

import type { Event } from '@/types/Event.dto'
import type { EventVM } from '@/view-models/event/EventVM'

export function useEvents(): {
  events: EventVM[]
  loading: boolean
} {
  const [data, setData] = useState<Event[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let mounted = true

    async function load() {
      setLoading(true)
      try {
        const result = await fetchEvents()
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

  const events = useMemo(() => {
    return data.map(mapEventToVM)
  }, [data])

  return { events, loading }
}
