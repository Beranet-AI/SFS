import type { Event } from '@/types/Event.dto'
import { http } from './event'

const BASE = process.env.NEXT_PUBLIC_MANAGEMENT_API!

/**
 * Fetch active alerts (mapped as events in UI)
 */
export async function fetchEvents(): Promise<Event[]> {
  try {
    return await http<Event[]>(`${BASE}/api/v1/alerts/active/`)
  } catch (err) {
    console.error('fetchEvents failed:', err)
    return []
  }
}
