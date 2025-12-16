'use client'

import { createContext, useContext, useMemo } from 'react'

import type { LiveStatus } from '@/types/LiveStatus.dto'
import type { Incident } from '@/types/Incident.dto'
import {
  incidentToLiveStatus,
  liveStatusPolicy,
} from '@/policies/live-status/liveStatusPolicy'
import { playCriticalLiveStatusSound } from '@/ui/shared/sounds/liveStatusSound'

interface LiveStatusContextValue {
  statuses: LiveStatus[]
}

const LiveStatusContext = createContext<LiveStatusContextValue | null>(null)

export function LiveStatusProvider({
  children,
  events = [],
}: {
  children: React.ReactNode
  events?: Incident[]
}) {
  const statuses = useMemo(() => {
    const nextStatuses = events
      .filter(liveStatusPolicy)
      .map(incidentToLiveStatus)

    if (nextStatuses.some((status) => status.severity === 'critical')) {
      playCriticalLiveStatusSound()
    }

    return nextStatuses
  }, [events])

  return (
    <LiveStatusContext.Provider value={{ statuses }}>
      {children}
    </LiveStatusContext.Provider>
  )
}

export function useLiveStatusContext() {
  const ctx = useContext(LiveStatusContext)
  if (!ctx) {
    throw new Error(
      'useLiveStatusContext must be used inside LiveStatusProvider',
    )
  }
  return ctx
}
