'use client'

import { useEffect, useRef } from 'react'
import { toast } from 'sonner'
import type { LiveStatus } from '@/types/LiveStatus.dto'

export function useStatusToasts(statuses: LiveStatus[]) {
  const shownRef = useRef<Set<string>>(new Set())

  useEffect(() => {
    statuses.forEach((status) => {
      if (shownRef.current.has(status.id)) return

      shownRef.current.add(status.id)

      const metric = status.payload?.metric?.toUpperCase() ?? 'STATUS'
      const description =
        status.payload?.value !== undefined
          ? `Value: ${status.payload.value}`
          : 'Status change detected'

      const title = `${metric} Status`

      if (status.severity === 'critical') {
        toast.error(title, {
          description,
          duration: Infinity,
        })
      } else if (status.severity === 'warning') {
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
  }, [statuses])
}
