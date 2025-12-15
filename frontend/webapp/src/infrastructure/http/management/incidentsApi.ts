import type { Incident } from '@/types/incidentDto'
import { http } from '../event'

const BASE = process.env.NEXT_PUBLIC_MANAGEMENT_API!

/**
 * Fetch active incidents (management domain)
 */
export async function fetchIncidents(): Promise<Incident[]> {
  try {
    return await http<Incident[]>(`${BASE}/api/v1/alerts/active/`)
  } catch (err) {
    console.error('fetchIncidents failed:', err)
    return []
  }
}
