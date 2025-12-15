'use client'

import { useEffect, useRef } from 'react'
import { toast } from 'sonner'
import type { liveEvent } from '@/types/Event.dto'

export function useAlertToasts(alerts: liveEvent[]) {
  const shownRef = useRef<Set<string>>(new Set())

  useEffect(() => {
    alerts.forEach((alert) => {
      if (shownRef.current.has(alert.id)) return

      shownRef.current.add(alert.id)

      const title = `${alert.payload.metric.toUpperCase()} Alert`
      const description = `Value: ${alert.payload.value}`

      if (alert.severity === 'critical') {
        toast.error(title, {
          description,
          duration: Infinity,
        })
      } else if (alert.severity === 'warning') {
        toast.warning(title, {
          description,
          duration: 6000,
        })
      } else {
        toast.info(title, {
          description,
          duration: 4000,
        })
      }
    })
  }, [alerts])
}
