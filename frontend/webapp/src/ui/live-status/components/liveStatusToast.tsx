'use client'

import { LiveStatus } from '@/types/liveStatusDto'

export function LiveStatusToast({ status }: { status: LiveStatus }) {
  const color =
    status.severity === 'critical'
      ? 'bg-red-600'
      : status.severity === 'warning'
        ? 'bg-yellow-500'
        : 'bg-blue-500'

  return (
    <div className={`${color} text-white px-4 py-3 rounded shadow`}>
      <div className="font-semibold">{status.title}</div>
      <div className="text-sm">{status.message}</div>
    </div>
  )
}
