import type { Alert } from '@/types/Alert.dto'
import { http } from './device'

const BASE = process.env.NEXT_PUBLIC_MANAGEMENT_API!

export function fetchAlerts(): Promise<Alert[]> {
  return http<Alert[]>(`${BASE}/alerts/`)
}

export function ackAlert(id: string): Promise<Alert> {
  return http<Alert>(`${BASE}/alerts/${id}/ack/`, { method: 'POST' })
}

export function resolveAlert(id: string): Promise<Alert> {
  return http<Alert>(`${BASE}/alerts/${id}/resolve/`, { method: 'POST' })
}
