'use client'

import { createContext, useContext, useMemo } from 'react'

import type { Alert } from '@/types/Alert.dto'
import type { Event } from '@/types/Event.dto'
import { eventToAlert, alertPolicy } from '@/policies/alert/alertPolicy'
import { playCriticalAlertSound } from '@/ui/shared/sounds/AlertSound'

interface AlertContextValue {
  alerts: Alert[]
}

const AlertContext = createContext<AlertContextValue | null>(null)

export function AlertProvider({
  children,
  events = [],
}: {
  children: React.ReactNode
  events?: Event[]
}) {
  const alerts = useMemo(() => {
    const nextAlerts = events.filter(alertPolicy).map(eventToAlert)

    if (nextAlerts.some((a) => a.level === 'critical')) {
      playCriticalAlertSound()
    }

    return nextAlerts
  }, [events])

  return (
    <AlertContext.Provider value={{ alerts }}>{children}</AlertContext.Provider>
  )
}

export function useAlertContext() {
  const ctx = useContext(AlertContext)
  if (!ctx) {
    throw new Error('useAlertContext must be used inside AlertProvider')
  }
  return ctx
}
