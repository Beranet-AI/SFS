'use client'

import { Alert } from '@/types/Alert.dto'

export function AlertToast({ alert }: { alert: Alert }) {
  const color =
    alert.severity === 'critical'
      ? 'bg-red-600'
      : alert.severity === 'warning'
        ? 'bg-yellow-500'
        : 'bg-blue-500'

  return (
    <div className={`${color} text-white px-4 py-3 rounded shadow`}>
      <div className="font-semibold">{alert.title}</div>
      <div className="text-sm">{alert.message}</div>
    </div>
  )
}
