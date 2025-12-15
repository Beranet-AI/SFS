'use client'

import type { Alert } from '@/types/Alert.dto'
import { useAlerts } from '@/ui/alert/hooks/useAlerts'

interface Props {
  alerts: Alert[]
}

export function AlertIndicator({ alerts }: Props) {
  const alertVMs = useAlerts(alerts)

  return (
    <div className="space-y-2">
      {alertVMs.map((alert) => (
        <div
          key={alert.id}
          className={`rounded p-3 border border-${alert.color}-400 bg-${alert.color}-50`}
        >
          <strong>{alert.title}</strong>
          <p className="text-sm">{alert.message}</p>
        </div>
      ))}
    </div>
  )
}
