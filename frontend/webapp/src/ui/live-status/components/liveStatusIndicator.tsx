'use client'

import type { LiveStatus } from '@/types/LiveStatus.dto'
import { mapLiveStatusToVM } from '@/mappers/live-status/liveStatusMapper'

interface Props {
  statuses: LiveStatus[]
}

export function LiveStatusIndicator({ statuses }: Props) {
  const statusVMs = statuses.map(mapLiveStatusToVM)

  return (
    <div className="space-y-2">
      {statusVMs.map((status) => (
        <div
          key={status.id}
          className={`rounded p-3 border border-${status.color}-400 bg-${status.color}-50`}
        >
          <strong>{status.title}</strong>
          <p className="text-sm">{status.message}</p>
        </div>
      ))}
    </div>
  )
}
