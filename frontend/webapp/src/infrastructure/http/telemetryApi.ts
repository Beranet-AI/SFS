import type { TelemetryReading } from '@/types/Telemetry.dto'
import { http } from './event'

const BASE = process.env.NEXT_PUBLIC_MANAGEMENT_API!

/**
 * Fetch latest telemetry readings for dashboard
 */
export async function fetchTelemetry(): Promise<TelemetryReading[]> {
  try {
    return await http<TelemetryReading[]>(
      `${BASE}/api/v1/dashboard/latest-readings/`,
    )
  } catch (err) {
    console.error('fetchTelemetry failed:', err)
    return []
  }
}
