'use client'

import { useEffect, useState } from 'react'
import { Incident, LiveStatus } from '@/types'
import { incidentToLiveStatus } from '@/policies/live-status/liveStatusPolicy'
import { shouldPlaySound } from '@/policies/live-status/liveStatusSoundPolicy'
import { playCriticalLiveStatusSound } from '@/ui/shared/sounds/liveStatusSound'

const BASE = process.env.NEXT_PUBLIC_MANAGEMENT_API!

export function useLiveStatuses() {
  const [statuses, setStatuses] = useState<LiveStatus[]>([])

  useEffect(() => {
    const interval = setInterval(async () => {
      const res = await fetch(`${BASE}/api/v1/events/`)
      const events: Incident[] = await res.json()

      const newStatuses = events
        .filter((e) => e.status === 'raised')
        .map(incidentToLiveStatus)

      setStatuses(newStatuses)

      newStatuses.forEach((status) => {
        if (shouldPlaySound(status)) {
          playCriticalLiveStatusSound()
        }
      })
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  return statuses
}
