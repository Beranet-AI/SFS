'use client'

import { useEffect, useState } from 'react'
import { Event, Alert } from '@/types'
import { eventToAlert } from '@/policies/alert/alertPolicy'
import { shouldPlaySound } from '@/policies/alert/alertSoundPolicy'
import { playCriticalAlertSound } from '@/ui/shared/sounds/AlertSound'

const BASE = process.env.NEXT_PUBLIC_MANAGEMENT_API!

export function useAlerts() {
  const [alerts, setAlerts] = useState<Alert[]>([])

  useEffect(() => {
    const interval = setInterval(async () => {
      const res = await fetch(`${BASE}/api/v1/events/`)
      const events: Event[] = await res.json()

      const newAlerts = events
        .filter((e) => e.status === 'raised')
        .map(eventToAlert)

      setAlerts(newAlerts)

      newAlerts.forEach((a) => {
        if (shouldPlaySound(a)) {
          playCriticalAlertSound()
        }
      })
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  return alerts
}
