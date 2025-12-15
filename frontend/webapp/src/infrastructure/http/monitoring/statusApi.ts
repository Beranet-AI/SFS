import type { LiveStatus } from '@/types/liveStatusDto'
import { http } from '../device'

const BASE = process.env.NEXT_PUBLIC_MANAGEMENT_API!

export function fetchLiveStatus(): Promise<LiveStatus[]> {
  return http<LiveStatus[]>(`${BASE}/alerts/`)
}

export function ackLiveStatus(id: string): Promise<LiveStatus> {
  return http<LiveStatus>(`${BASE}/alerts/${id}/ack/`, { method: 'POST' })
}

export function resolveLiveStatus(id: string): Promise<LiveStatus> {
  return http<LiveStatus>(`${BASE}/alerts/${id}/resolve/`, { method: 'POST' })
}
